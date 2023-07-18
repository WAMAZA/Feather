import os
import shutil

from . import app
from flask import render_template, request, redirect, url_for, send_file, session, json, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, AddPubForm, changePasswordForm, ChangePubForm, ContactForm
from .models import User, Publication, Livre, Commentaire, Liked, Messages
from .database import db
from werkzeug.utils import secure_filename
from datetime import date, timedelta

def hasChanged(str1, str2):
    return str1.strip() != str2.strip()

@app.errorhandler(403)
def not_allowed(e):
    return render_template('error.html', status=403, message="Oups... Vous n'êtes pas autorisé à être ici", user=current_user), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', status=404, message="Oups... Page introuvable", user=current_user), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', status=500, message="Erreur du serveur", user=current_user), 500

@app.route('/')
def accueil():
    liked_pubs = Publication.query.all()
    recent_pubs = Publication.query.all()
    liked_pubs.sort(key=lambda x: x.nb_like, reverse=True)
    recent_pubs.sort(key=lambda x: x.pub_date, reverse=True)

    return render_template("accueil.html", user=current_user, liked_pubs=liked_pubs[:3], recent_pubs=recent_pubs)

@app.route("/like/<npub>", methods=["POST", "GET"])
def like(npub):
    current_pub = Publication.query.get(npub)
    if request.method == "POST":
        data = json.loads(request.data)
        current_pub.nb_like = data.get("nb_like")

        if data.get("result") == "increment":
            db.session.add(Liked(ncli=current_user.ncli, npub=npub))
            Publication.compute_nb_like(current_pub)
        elif data.get("result") == "decrement":
            db.session.delete(Liked.query.get((current_user.ncli, npub)))
            Publication.compute_nb_like(current_pub)
        db.session.commit()
    return redirect(url_for("accueil"))

# Système de compte (Connexion, Inscription, Deconnexion)
@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    form = LoginForm()
    nextPage = request.args.get("next")

    # Check if the current user is already logged in
    if current_user.is_authenticated:
        redirect("/")

    if request.method == 'GET':
        return render_template('login.html', form=form, user=current_user, error=None, nextPage=nextPage)
    if not form.validate_on_submit():
        return render_template('login.html', form=form, user=current_user, error=None, nextPage=nextPage)

    user = User.query.filter_by(username=(form.user_name.data)).first()

    if user is None:
        error = "Nom d'utilisateur incorrect"
        return render_template('login.html', form=form, user=current_user, error=error, nextPage=nextPage)
    else:
        if not user.check_password(form.passwd.data):
            error = "Mot de passe incorrect"
            return render_template('login.html', form=form, user=current_user, error=error, nextPage=nextPage)

        elif user.state == "inactive":
            error = "Votre compte est bloqué"
            return render_template('login.html', form=form, user=current_user, error=error, nextPage=nextPage)
        else:
            login_user(user, remember=True, force=True)
            next = request.args.get('next')
            if (next in ["", None]):
                return redirect(url_for('espace_membre'))
            return redirect(next)


@app.route("/inscription", methods=["POST", "GET"])
def inscription():
    form = RegisterForm()
    # Set minimum age to register to the service
    minAge = 12
    # Compute the maximum birth_day date
    birthDateMaxRequired = date.today() - timedelta(days= minAge*365)

    if request.method == 'GET':
        return render_template('register.html', form=form, user=current_user, maxDate= birthDateMaxRequired.strftime("%Y-%m-%d"))
    if not form.validate_on_submit():
        return render_template('register.html', form=form, user=current_user, maxDate= birthDateMaxRequired.strftime("%Y-%m-%d"))

    # create user
    if not form.validate_username(form.user_name):
        error = "Le nom d'utilisateur est déjà utilisé !"
        return render_template('register.html', form=form, error=error, user=current_user)
    if not form.validate_email(form.email):
        error = "L'adresse mail est déjà utilisée !"
        return render_template('register.html', form=form, error=error, user=current_user)
    else:
        if form.validate_email(form.email):
            new_user = User(last_name=form.last_name.data, first_name=form.first_name.data,
                            email=form.email.data, username=(form.user_name.data), birthday=form.birthday.data,
                            group="normal", state="actif")
            new_user.set_password(form.passwd.data)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True, force=True)
            return redirect(url_for('espace_membre'))
        else:
            error = "L'adresse mail est déjà utilisé !"
            return render_template('register.html', form=form, error=error, user=current_user)


@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('accueil'))


# Espace membre
@app.route("/espace_membre", methods=["POST", "GET"])
@login_required
def espace_membre():
    minAge = 12
    birthDateMaxRequired = date.today() - timedelta(days= minAge*365)
    pubs = Publication.query.filter_by(ncli=current_user.ncli).all()

    myComments = Commentaire.query.filter_by(ncli=current_user.ncli).all()
    print(myComments)
    myComments.sort(key=lambda x: x.comment_date, reverse=True)
    print(myComments)
    liked = []
    allPub = Publication.query.all()
    for all_pubs in allPub:
        if Publication.isLiked(all_pubs, current_user):
            liked.append(all_pubs)

    if session.get("success"):
        # store the sessions success message into a simple variable
        success = session["success"]
        # clear the sesssion variable
        session.pop("success")
        return render_template("member_space.html", user=current_user, success=success, pubs=pubs,
                               myComments=myComments, liked=liked, allPub=allPub,maxDate= birthDateMaxRequired.strftime("%Y-%m-%d"))
    else:
        return render_template("member_space.html", user=current_user, success=None, pubs=pubs,
                               myComments=myComments, liked=liked,allPub=allPub,maxDate= birthDateMaxRequired.strftime("%Y-%m-%d"))


@app.route("/change_info", methods=["POST", "GET"])
@login_required
def changeInfo():
    user = User.query.filter_by(ncli=current_user.ncli).first()
    if request.method == "POST":
        # récupere les valeurs envoyer par la requete ajax
        last_name = request.form["last_name"]
        first_name = request.form["first_name"]
        username = request.form["username"]
        email = request.form["email"]
        birthday = request.form["birthday"]

        # remplace dans la BD
        user.last_name = last_name
        user.first_name = first_name
        user.username = username
        user.email = email
        user.birthday = birthday

        # update dans la BD
        db.session.commit()

    return redirect(url_for('espace_membre'))


@app.route("/change_password", methods=["POST", "GET"])
@login_required
def changePassword():
    form = changePasswordForm()
    user = User.query.get(current_user.ncli)
    pubs = Publication.query.filter_by(ncli=current_user.ncli).all()
    if request.method == 'GET':
        return render_template('change_passwd.html', form=form, user=current_user, pubs=pubs)
    if not form.validate_on_submit():
        return render_template('change_passwd.html', form=form, user=current_user, pubs=pubs)

    old_passwd = form.old_password.data
    new_passwd = form.new_password.data

    if not user.check_password(old_passwd):
        return render_template('change_passwd.html', form=form, user=current_user,
                               error="L'ancien mot de passe est incorrect !", pubs=pubs)
    elif user.check_password(new_passwd):
        return render_template('change_passwd.html', form=form, user=current_user,
                               error="Vous ne pouvez pas utiliser le même mot de passe qu'avant.",pubs=pubs)
    else:
        user.set_password(new_passwd)

        db.session.commit()

        # create a session variable for the success message
        session['success'] = "Mot de passe changé avec succès !"

        return redirect(url_for("espace_membre"))


# add/modify/delete Publication
@app.route("/ajout_publication", methods=["POST", "GET"])
@login_required
def ajout_pub():
    form = AddPubForm()

    if request.method == 'GET':
        return render_template('add_publication.html', form=form, user=current_user)
    if not form.validate_on_submit():
        return render_template('add_publication.html', form=form, user=current_user)

    last_npub = Publication.query.count()
    # upload du fichier pdf
    filename = secure_filename(form.ajout_pdf.data.filename)
    # create the directory
    new_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], str(last_npub + 1))
    if os.path.exists(new_folder_path):
        shutil.rmtree(new_folder_path)
    os.mkdir(new_folder_path)
    # add the file to the directory
    form.ajout_pdf.data.save(os.path.join(app.config['UPLOAD_FOLDER'], str(last_npub + 1), filename))
    # get the path of the file to put it in the database
    filename_path = os.path.join(app.config['UPLOAD_FOLDER'], str(last_npub + 1), filename)

    # upload du ficher image
    filename2 = secure_filename(form.ajout_img.data.filename)
    # create the directory
    # changer le ARTAK par celui de la version finale
    new_d = os.path.join(os.getcwd(), "my_app/static/img/product", str(last_npub + 1))
    if os.path.exists(new_d):
        shutil.rmtree(new_d)

    os.mkdir(new_d)
    # add the file to the directory
    form.ajout_img.data.save(os.path.join(new_d, filename2))
    # get the path of the file to put it in the database
    filename2_path = os.path.join(url_for("static", filename="img/product/%s/%s" % (str(last_npub + 1), filename2)))

    # update de la BD pour la table Livre
    livre = Livre(titre=form.titre.data, auteur=form.auteur.data,
                  resume=form.resume.data, pdf_link=filename_path,
                  image_link=filename2_path)

    db.session.add(livre)
    db.session.commit()

    # update de la BD pour la table Publication
    pub = Publication(ncli=current_user.ncli, nlivre=livre.nlivre,
                      nb_like=0, nb_download=0, pub_date=date.today())

    db.session.add(pub)
    db.session.commit()

    return redirect(url_for("espace_membre"))


@app.route("/modifier_publication/<npub>", methods=["POST", "GET"])
@login_required
def modifier_pub(npub):
    form = ChangePubForm()
    book = Livre.query.filter_by(nlivre=npub).first()

    if request.method == 'GET':
        if not Publication.query.filter_by(npub=npub, ncli=current_user.ncli).first():
            abort(403)
        else:
            return render_template('modify_publication.html', form=form, user=current_user, book=book)
    if not form.validate_on_submit():
        return render_template('modify_publication.html', form=form, user=current_user, book=book)

    # récuperation des nouveaux donnée
    titre = form.titre.data
    auteur = form.auteur.data
    resume = form.resume.data

    # récuperation des noms des nouveaux fichier
    pdf_filename = secure_filename(form.ajout_pdf.data.filename)
    img_filename = secure_filename(form.ajout_img.data.filename)

    # Changer ARTAK pour la version finale
    img_folder = os.path.join(os.getcwd(), "my_app/static/img/product", npub)
    pdf_folder = os.path.join(os.getcwd(), "uploaded_files/product", npub)

    # Supprimer tous les éléments des anciens répertoire pour les remplacer par les nouveaux
    if len(img_filename) > 0:
        for file in os.listdir(img_folder):
            file_path = os.path.join(os.getcwd(), "my_app/static/img/product", npub, file)
            if os.path.exists(file_path):
                os.unlink(file_path)

    if len(pdf_filename) > 0:
        for file in os.listdir(pdf_folder):
            file_path = os.path.join(os.getcwd(), "uploaded_files/product", npub, file)
            if os.path.exists(file_path):
                os.unlink(file_path)

    # Ajouter les nouveaux fichiers
    if len(img_filename) > 0:
        form.ajout_img.data.save(os.path.join(str(img_folder), img_filename))
    if len(pdf_filename) > 0:
        form.ajout_pdf.data.save(os.path.join(str(pdf_folder), pdf_filename))

    # création des nouveau lien pour la BD
    if len(img_filename) > 0:
        new_img_link = os.path.join("/static/img/product", npub, img_filename)
    if len(pdf_filename) > 0:
        new_pdf_link = os.path.join(os.getcwd(), "uploaded_files/product", npub, pdf_filename)


    # mise à jour dans la BD
    if hasChanged(book.titre, titre):
        book.titre = titre
    if hasChanged(book.auteur, auteur):
        book.auteur = auteur
    if hasChanged(book.resume, resume):
        book.resume = resume
    if len(img_filename) > 0:
        book.image_link = new_img_link
    if len(pdf_filename) > 0:
        print(new_pdf_link)
        book.pdf_link = new_pdf_link

    db.session.commit()

    return redirect(url_for("espace_membre"))


@app.route("/supprimer_publication/<npub>", methods=["POST", "GET"])
@login_required
def supprimer_pub(npub):
    get_pub = Publication.query.get(npub)
    get_book = Livre.query.get(npub)
    get_liked = Liked.query.filter_by(npub=npub).all()
    get_comments = Commentaire.query.filter_by(npub=npub).all()

    if not Publication.query.filter_by(npub=npub, ncli=current_user.ncli).first():
        abort(403)


    if request.method == "POST":
        # delete pub
        db.session.delete(get_pub)

        # delete book
        db.session.delete(get_book)

        # delete all likes
        for likes in get_liked:
            db.session.delete(likes)

        # delete all comments
        for comments in get_comments:
            db.session.delete(comments)

        db.session.commit()
        return redirect(url_for("espace_membre"))
    else:
        abort(403)


# Product // add comment at the same time with addCommentForm()
@app.route("/produit/<npub>", methods=["GET", "POST"])
def produit(npub):
    pub = Publication.query.filter_by(npub=npub).first()
    avis = Commentaire.query.filter_by(npub=npub).all()
    avis.sort(key=lambda x: x.ncom, reverse=True)
    return render_template("product.html", user=current_user, pub=pub, avis=avis)


@app.route("/telecharger/produit/<npub>")
def telecharger_produit(npub):
    npub_path = Livre.query.filter_by(nlivre=npub).first()
    path = npub_path.pdf_link
    pub = Publication.query.filter_by(npub=npub).first()
    pub.nb_download += 1

    # Create new placeholder file if no pdf is in database
    if not os.path.exists(path):
        path = os.path.join(app.config["UPLOAD_FOLDER"],"default","%s.txt"%npub_path.titre)
        if not os.path.exists(path):
            createFile(path)

    db.session.commit()
    return send_file(path, as_attachment=True)

def createFile(path: str) -> bool:
    f = open(path, "w+")
    f.write(" PDF!\n")
    f.close()

# Comment
@app.route("/ajout_commentaire/<npub>", methods=["GET", "POST"])
@login_required
def ajout_commentaire(npub):
    if request.method == "POST":
        # récupere les valeurs envoyer par la requete ajax
        avis = request.form["avis_text"]
        note = request.form["avis_note"]

        # création de l'objet pour le commentaire
        new_comment = Commentaire(ncli=current_user.ncli, npub=npub, contenu=avis, comment_date=date.today(), note=note)

        db.session.add(new_comment)
        # update dans la BD
        db.session.commit()

    # compute the new note of the publication
    concerned_pub = Publication.query.get(npub)
    Publication.compute_note(concerned_pub)
    db.session.commit()

    return redirect(url_for('produit', npub=npub))


@app.route('/bibliotheque')
def bibliotheque():
    return render_template("bibliotheque.html", user=current_user, pubs=Publication.query.all())


@app.route('/contact', methods=["POST", "GET"])
def contact():
    form = ContactForm()

    if request.method == 'GET':
        return render_template('contact.html', form=form, user=current_user, error=None)
    if not form.validate_on_submit():
        return render_template('contact.html', form=form, user=current_user, error=None)

    nom = form.nom.data
    prenom = form.prenom.data
    email = form.email.data
    message = form.message.data
    if current_user.is_authenticated:
        num_cli = current_user.ncli
    else:
        num_cli = None

    Contact = Messages(nom=nom, prenom=prenom,
                       email=email, message=message,nb_cli=num_cli)

    db.session.add(Contact)
    db.session.commit()

    return redirect(url_for("accueil"))


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html", user=current_user, users=User.query.all(), publications=Publication.query.all())

@app.route('/update_user_status', methods=['POST'])
def update_user_status():

    user_id = request.form['user_id']
    new_status = request.form['new_status']

    user = User.query.get(user_id)

    user.state = new_status
    db.session.commit()

    return redirect(url_for("admin"))


@app.route('/update_user_group', methods=['POST'])
def update_user_group():
    user_id = request.form['user_id']
    new_group = request.form['new_group']

    user = User.query.get(user_id)

    user.group = new_group
    db.session.commit()

    return redirect(url_for("admin"))

@app.route('/delete_user/<user_id>', methods=['POST', "GET"])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        # delete user's comments
        user_comments = Commentaire.query.filter_by(ncli=user.ncli).all()
        for comments in user_comments:
            db.session.delete(comments)

        # delete user's publication
        user_pub = Publication.query.filter_by(ncli=user.ncli).all()
        for pub in user_pub:
            db.session.delete(pub)

        # delete user's likes
        user_like = Liked.query.filter_by(ncli=user.ncli).all()
        for likes in user_like:
            db.session.delete(likes)

        # delete user
        db.session.delete(user)

        # commit the database
        db.session.commit()
        return redirect(url_for('accueil'))
    else:
        flash('Error: User not found')

    if request.referrer == url_for("admin"):
        return redirect(url_for('admin'))
    elif request.referrer == url_for("espace_membre"):
        return redirect(url_for("accueil"))