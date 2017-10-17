# -*- coding: utf-8 -*-
"""Unit tests for Collection model."""

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime as dt

import pytest
from six import string_types

from xl_auth.collection.models import Collection
from xl_auth.permission.models import Permission

from ..factories import CollectionFactory


@pytest.mark.usefixtures('db')
def test_get_by_id():
    """Get collection by ID."""
    collection = Collection(code='SKB', friendly_name='Literature by Strindberg',
                            category='bibliography')
    collection.save()

    retrieved = Collection.get_by_id(collection.id)
    assert retrieved == collection


@pytest.mark.usefixtures('db')
def test_created_at_defaults_to_datetime():
    """Test creation date."""
    collection = Collection('KBX', 'Secret books', 'library')
    collection.save()
    assert bool(collection.created_at)
    assert isinstance(collection.created_at, dt.datetime)


@pytest.mark.usefixtures('db')
def test_factory(db):
    """Test collection factory."""
    collection = CollectionFactory()
    db.session.commit()
    assert isinstance(collection.code, string_types)
    assert isinstance(collection.friendly_name, string_types)
    assert collection.category in {'bibliography', 'library', 'uncategorized'}
    assert collection.active is True
    assert collection.replaces is None
    assert collection.replaced_by is None
    assert isinstance(collection.permissions, list)
    assert bool(collection.created_at)


@pytest.mark.usefixtures('db')
def test_adding_permissions(user):
    """Add a permission on the collection."""
    collection = CollectionFactory()
    collection.save()
    permission = Permission(user=user, collection=collection)
    permission.save()

    assert permission in collection.permissions


@pytest.mark.usefixtures('db')
def test_removing_permissions(user):
    """Remove the permissions an a collection."""
    collection = CollectionFactory()
    collection.save()
    permission = Permission(user=user, collection=collection)
    permission.save()
    permission.delete()

    assert permission not in collection.permissions


@pytest.mark.usefixtures('db')
def test_repr():
    """Check repr output."""
    collection = CollectionFactory(code='KBZ')
    assert repr(collection) == '<Collection({!r})>'.format('KBZ')
