from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from . import app
import os
from datetime import date


class User(UserMixin, db.Model):
    __tablename__ = "users"

    ncli = db.Column(db.Integer, primary_key=True, autoincrement=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    birthday = db.Column(db.String(15), nullable=False)
    password_hash = db.Column(db.String(128))
    pub = db.relationship('Publication', backref='user')
    group = db.Column(db.String(6), nullable=False)
    state = db.Column(db.String(6), nullable=False)
    myLikes = db.relationship("Liked", backref="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return (self.ncli) 


class Publication(db.Model):
    __tablename__ = "publication"

    npub = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ncli = db.Column(db.Integer, db.ForeignKey("users.ncli"))
    nlivre = db.Column(db.Integer, db.ForeignKey("livre.nlivre"))
    nb_like = db.Column(db.Integer, nullable=True, default=0)
    nb_download = db.Column(db.Integer, nullable=True, default=0)
    pub_date = db.Column(db.String(15), nullable=False)
    note = db.Column(db.Integer, default=0, nullable=True)
    livre = db.relationship("Livre", backref="publication")
    comments = db.relationship("Commentaire", backref="publication")

    def isLiked(self, user):
        return Liked.query.filter_by(ncli=user.ncli, npub=self.npub).first()

    def compute_nb_like(self):
        result = Liked.query.filter_by(npub=self.npub).count()

        if result == 0:
            self.nb_like = 0
        else:
             self.nb_like = result

    def compute_note(self):
        all_comment = Commentaire.query.filter_by(npub=self.npub).all()
        sum_note = 0
        for i in all_comment:
            sum_note += i.note
        if len(all_comment) != 0:
            result = self.note = sum_note / len(all_comment)
        else:
            result = 0
        return result


class Livre(db.Model):
    __tablename__ = "livre"

    nlivre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(30), nullable=False)
    resume = db.Column(db.String(1000), nullable=False)
    pdf_link = db.Column(db.String(150), nullable=False)
    image_link = db.Column(db.String(150), nullable=False)


class Commentaire(db.Model):
    __tablename__ = "commentaire"

    ncom = db.Column(db.Integer, primary_key=True)
    ncli = db.Column(db.Integer, db.ForeignKey("users.ncli"), nullable=False)
    npub = db.Column(db.Integer, db.ForeignKey("publication.npub"), nullable=False)
    contenu = db.Column(db.String(1000), nullable=False)
    comment_date = db.Column(db.String(15), nullable=False)
    note = db.Column(db.Integer, nullable=False, default=0)
    user = db.relationship("User", backref="commentaire")

class Liked(db.Model):
    __tablename__ = "liked"

    ncli = db.Column(db.Integer, db.ForeignKey('users.ncli'), nullable=False, primary_key=True)
    npub = db.Column(db.Integer, db.ForeignKey('publication.npub'), nullable=False, primary_key=True)

class Messages(db.Model):
    __tablename__ = "messages"

    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    nb_msg = db.Column(db.Integer, nullable=False, primary_key=True)
    nb_cli = db.Column(db.Integer, db.ForeignKey('users.ncli'), nullable=True)

with app.app_context():
    db.drop_all()
    db.create_all()

    # add admin user by default
    user = User(last_name="last name admin", first_name="first name admin", email="emailadmin@gmail.com", username="admin",
                birthday="2000-01-01", group="admin", state="actif")
    user.set_password("password")
    user1 = User(last_name="last name user", first_name="first name user", email="emailuser@gmail.com", username="user",
                birthday="2000-01-01", group="normal", state="actif")
    user1.set_password("password")
    db.session.add_all([user, user1])
    db.session.commit()

    # add books
    book1 = Livre(titre="Madame Bovary", auteur="Gustave Flaubert", resume="Il y a peu de femmes que, de tête au moins, je n'aie déshabillées jusqu'au talon. J'ai travaillé la chair en artiste et je la connais. Quant à l'amour, ç'a été le grand sujet de réflexion de toute ma vie. Ce que je n'ai pas donné à l'art pur, au métier en soi, a été là et le cœur que j'étudiais c'était le mien. Flaubert défend ainsi son œuvre dans une lettre à sa maîtresse, Louise Collet. L'amour si quotidien de Charles Bovary, les passions tumultueuses de sa femme Emma étaient décrites avec tant de réalisme que lauteur et l'imprimeur furent traînés en justice pour offense publique à la morale et à la religion. On les acquitta. Flaubert n'avait peint que la réalité, les moisissures de l'âme. Une femme, mal mariée, dans une petite ville normande, rêve d'amour et le trouve.",
                 image_link= "/static/img/product/1/img.jpeg", pdf_link=os.path.join(os.getcwd(), "uploaded_files/product/1/Flaubert-Bovary-pdf.pdf"))

    book2 = Livre(titre="Frankenstein", auteur="Mary Shelley", resume="Victor Frankenstein, scientifique genevois, est recueilli sur la banquise par un équipage faisant route vers le Pôle Nord. Très tourmenté, il livre son histoire au capitaine du bateau : quelque temps auparavant, il est parvenu à donner la vie à une créature surhumaine. Mais celle-ci sème bientôt la terreur autour d'elle...En expédition vers le pôle Nord, Robert Walton adresse à sa sœur des lettres où il évoque l'étrange spectacle dont il vient d'être le témoin depuis son bateau : la découverte, sur un iceberg, d'un homme en perdition dans son traîneau. Invité à monter à bord, Victor Frankenstein raconte qu'il n'est venu s’aventurer ici que pour rattraper quelqu'un - qui n'est autre que la créature monstrueuse qu'il créa naguère, et qui s'est montrée redoutablement criminelle.",
                 image_link="/static/img/product/2/img.jpeg", pdf_link=os.path.join(os.getcwd(), "uploaded_files/product/2/Frankenstein_Mary_Shelley.pdf"))

    book3 = Livre(titre="L'assassin Royal - L'apprenti assassin", auteur="Robin Hobb", resume="Au château de Castelcerf le roi Subtil Loinvoyant règne sur les Six Duchés ; il est aidé dans sa lourde tâche par son fils Chevalerie qui, comme son père et tous les nobles du royaume, porte le nom de la qualité que ses parents espéraient le voir développer. Ainsi le frère du Roi-servant s'appelle-t-il Vérité et leur demi-frère, né d'un second lit, Royal. Suite à une aventure restée inconnue de tous, Chevalerie donne à la lignée un nouveau descendant : un bâtard, dont la simple existence va bouleverser le fragile équilibre qu'avait établi le roi pour contrôler ses turbulents fils. Ce héros malgré lui, nommé Fitz, voit son avenir s'assombrir au fil du temps. Alors que les autres enfants ont déjà leur place à la cour et dans ses intrigues, lui devra la mériter et servir la couronne en devenant ce que personne ne voulait être : l'Assassin royal. Au service de son roi, il apprendra les poisons, le meurtre et la trahison...",
                 image_link="/static/img/product/3/img.jpeg", pdf_link=os.path.join(os.getcwd(), "uploaded_files/product/3/Arsen_Lupin_Gentleman_Cambrioleur_Maurice_Leblanc.pdf"))

    book4 = Livre(titre="Madame Bovary", auteur="Gustave Flaubert",
                  resume="Il y a peu de femmes que, de tête au moins, je n'aie déshabillées jusqu'au talon. J'ai travaillé la chair en artiste et je la connais. Quant à l'amour, ç'a été le grand sujet de réflexion de toute ma vie. Ce que je n'ai pas donné à l'art pur, au métier en soi, a été là et le cœur que j'étudiais c'était le mien. Flaubert défend ainsi son œuvre dans une lettre à sa maîtresse, Louise Collet. L'amour si quotidien de Charles Bovary, les passions tumultueuses de sa femme Emma étaient décrites avec tant de réalisme que lauteur et l'imprimeur furent traînés en justice pour offense publique à la morale et à la religion. On les acquitta. Flaubert n'avait peint que la réalité, les moisissures de l'âme. Une femme, mal mariée, dans une petite ville normande, rêve d'amour et le trouve.",
                  image_link="/static/img/product/4/img.jpeg",
                  pdf_link=os.path.join(os.getcwd(), "uploaded_files/product/4/Flaubert-Bovary-pdf.pdf"))

    book5 = Livre(titre="Frankenstein", auteur="Mary Shelley",
                  resume="Victor Frankenstein, scientifique genevois, est recueilli sur la banquise par un équipage faisant route vers le Pôle Nord. Très tourmenté, il livre son histoire au capitaine du bateau : quelque temps auparavant, il est parvenu à donner la vie à une créature surhumaine. Mais celle-ci sème bientôt la terreur autour d'elle...En expédition vers le pôle Nord, Robert Walton adresse à sa sœur des lettres où il évoque l'étrange spectacle dont il vient d'être le témoin depuis son bateau : la découverte, sur un iceberg, d'un homme en perdition dans son traîneau. Invité à monter à bord, Victor Frankenstein raconte qu'il n'est venu s’aventurer ici que pour rattraper quelqu'un - qui n'est autre que la créature monstrueuse qu'il créa naguère, et qui s'est montrée redoutablement criminelle.",
                  image_link="/static/img/product/5/img.jpeg",
                  pdf_link=os.path.join(os.getcwd(), "uploaded_files/product/5/Frankenstein_Mary_Shelley.pdf"))

    book6 = Livre(titre="L'assassin Royal - L'apprenti assassin", auteur="Robin Hobb",
                  resume="Au château de Castelcerf le roi Subtil Loinvoyant règne sur les Six Duchés ; il est aidé dans sa lourde tâche par son fils Chevalerie qui, comme son père et tous les nobles du royaume, porte le nom de la qualité que ses parents espéraient le voir développer. Ainsi le frère du Roi-servant s'appelle-t-il Vérité et leur demi-frère, né d'un second lit, Royal. Suite à une aventure restée inconnue de tous, Chevalerie donne à la lignée un nouveau descendant : un bâtard, dont la simple existence va bouleverser le fragile équilibre qu'avait établi le roi pour contrôler ses turbulents fils. Ce héros malgré lui, nommé Fitz, voit son avenir s'assombrir au fil du temps. Alors que les autres enfants ont déjà leur place à la cour et dans ses intrigues, lui devra la mériter et servir la couronne en devenant ce que personne ne voulait être : l'Assassin royal. Au service de son roi, il apprendra les poisons, le meurtre et la trahison...",
                  image_link="/static/img/product/6/img.jpeg", pdf_link=os.path.join(os.getcwd(),
                                                                                     "uploaded_files/product/6/Arsen_Lupin_Gentleman_Cambrioleur_Maurice_Leblanc.pdf"))

    db.session.add_all([book1, book2, book3, book4, book5, book6])
    db.session.commit()

    # add publication
    pub1 = Publication(ncli=user.ncli, nlivre=book1.nlivre, pub_date="2022-12-01")
    pub2 = Publication(ncli=user.ncli, nlivre=book2.nlivre, pub_date="2022-12-01")
    pub3 = Publication(ncli=user.ncli, nlivre=book3.nlivre, pub_date="2022-12-01")
    pub4 = Publication(ncli=user.ncli, nlivre=book1.nlivre, pub_date="2022-12-01")
    pub5 = Publication(ncli=user.ncli, nlivre=book2.nlivre, pub_date="2022-12-01")
    pub6 = Publication(ncli=user.ncli, nlivre=book3.nlivre, pub_date="2022-12-01")
    db.session.add_all([pub1, pub2, pub3, pub4, pub5, pub6])
    db.session.commit()

    # add comment
    comment = Commentaire(ncli=user.ncli, npub=pub1.npub, contenu="Trop cool ce livre ! J'adore :)", comment_date=date.today(), note=3)
    comment2 = Commentaire(ncli=user.ncli, npub=pub1.npub, contenu="Trop cool ce livre ! J'adore :)",
                          comment_date=date.today(), note=5)

    db.session.add_all([comment, comment2])
    db.session.commit()

    # compute new note of each publication depends on the note of all comments
    pub1.compute_note()
    pub2.compute_note()
    pub3.compute_note()
    pub4.compute_note()
    pub5.compute_note()
    pub6.compute_note()
    db.session.commit()

    like1 = Liked(ncli=user.ncli, npub=pub3.npub)
    like2 = Liked(ncli=user1.ncli, npub=pub2.npub)
    db.session.add_all([like1, like2])
    db.session.commit()

    pub1.compute_nb_like()
    pub2.compute_nb_like()
    pub3.compute_nb_like()
    pub4.compute_nb_like()
    pub5.compute_nb_like()
    pub6.compute_nb_like()

    db.session.commit()