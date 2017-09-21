# -*- coding: utf-8 -*-
"""User forms."""

from __future__ import absolute_import, division, print_function, unicode_literals

from flask_babel import lazy_gettext as _
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User


class RegisterForm(Form):
    """User registration form."""

    username = StringField(_('Email'),
                           validators=[DataRequired(), Email(), Length(min=6, max=255)])
    full_name = StringField(_('Full name'), validators=[DataRequired(), Length(min=3, max=255)])
    password = PasswordField(_('Password'), validators=[DataRequired(), Length(min=6, max=64)])
    confirm = PasswordField(_('Verify password'),
                            validators=[DataRequired(),
                                        EqualTo('password', message=_('Passwords must match'))])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()

        if not initial_validation:
            return False

        user = User.query.filter_by(email=self.username.data).first()

        if user:
            self.username.errors.append(_('Email already registered'))
            return False

        return True
