from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, BooleanField, FileField, TextAreaField, SelectField
from wtforms.validators import Optional, Length, DataRequired, ValidationError, EqualTo, Email
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from .models import User

obligatoire = "Ce champ est obligatoire."
fichier = "Un fichier est requis."
name_validators = [DataRequired(message=obligatoire), Length(min=3, max=100, message="Ce champ doit être compris entre 3 et 100 caractères.")]
passwd_validators = [DataRequired(message=obligatoire), Length(min=8, message="Le mot de passe doit être de 8 caractères au minimum.")]
date_validators = [DataRequired(message=obligatoire)]
checkbox_validators = [DataRequired(message=obligatoire)]
email_validator = [DataRequired(message=obligatoire), Email("Ceci n'est pas une adresse mail")]
optional_field = [Optional()]
passwd_confirm_validators = [DataRequired(message=obligatoire), EqualTo('passwd', "Mauvais mot de passe de confirmation")]

class RegisterForm(FlaskForm):
    first_name = StringField(label="Prénom", validators=name_validators)
    last_name = StringField(label="Nom", validators=name_validators)
    email = StringField(label="Email", validators=email_validator)
    user_name = StringField(label="Nom d'utilisateur", validators=name_validators)
    birthday = DateField(label="Date de naissance", validators=date_validators)
    passwd = PasswordField(label='Mot de passe', validators=passwd_validators)
    passwd_confirm = PasswordField(label='Confirmer mot de passe', validators=passwd_confirm_validators)
    agree_terms = BooleanField("J'accepte les conditions générale du site", validators=checkbox_validators)
    submit = SubmitField(label='Inscription')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            excluded_chars = " *?!'^+%&/()=}][{$#"
            for char in self.user_name.data:
                if char in excluded_chars:
                    return False
        return True

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return False
        return True

class LoginForm(FlaskForm):
    user_name = StringField(label="Nom d'utilisateur", validators=name_validators)
    passwd = PasswordField(label='Mot de passe', validators=passwd_validators)
    submit = SubmitField(label='Connexion')

class AddPubForm(FlaskForm):
    titre = StringField(label="Titre", validators=name_validators)
    auteur = StringField(label="Auteur", validators=name_validators)
    resume = TextAreaField(label="Résumé", validators=[DataRequired(obligatoire)])
    ajout_pdf = FileField(label="Ajouter un fichier (PDF)", validators=[FileRequired(fichier), FileAllowed(["pdf"], "Seul les fichiers pdf sont acceptés")])
    ajout_img = FileField(label="Ajouter une couverture (PNG, JPG)", validators=[FileRequired(fichier), FileAllowed(["jpg", "png", "jpeg"], "Seul les fichiers .jpg et .png sont acceptés")])
    submit = SubmitField(label='Publier')

class ChangePubForm(FlaskForm):
    titre = StringField(label="Titre", validators=name_validators)
    auteur = StringField(label="Auteur", validators=name_validators)
    resume = TextAreaField(label="Résumé", validators=[DataRequired(obligatoire)])
    ajout_pdf = FileField(label="Ajouter un fichier (PDF)", validators=[FileAllowed(["pdf"], "Seul les fichiers pdf sont acceptés")])
    ajout_img = FileField(label="Ajouter une couverture (PNG, JPG)", validators=[FileAllowed(["jpg", "png", "jpeg"], "Seul les fichiers .jpg et .png sont acceptés")])
    submit = SubmitField(label='Modifier')

class changePasswordForm(FlaskForm):
    old_password = PasswordField(label="Ancien mot de passe", validators=passwd_validators)
    new_password = PasswordField(label="Nouveau mot de passe", validators=passwd_validators)
    retype_new_password = PasswordField(label="Retapez le nouveau mot de passe", validators=[DataRequired(message=obligatoire), EqualTo('new_password', "Mauvais mot de passe de confirmation")])
    submit = SubmitField(label='Modifier')

class ContactForm(FlaskForm):
    nom = StringField(label="Nom", validators=name_validators)
    prenom = StringField(label="Prénom", validators=name_validators)
    email = StringField(label="Email", validators=email_validator)
    message = TextAreaField(label="Message", validators=[DataRequired(obligatoire), Length(min=50, message="Un minimum de 50 caractères est requis.")])
    submit = SubmitField(label='Envoyer')