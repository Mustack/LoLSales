# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Champion.name'
        db.delete_column('champions_champion', 'name')

        # Deleting field 'Skin.name'
        db.delete_column('champions_skin', 'name')

        # Adding field 'Product.name'
        db.rename_column('champions_product', '_name', 'name')


    def backwards(self, orm):
        # Adding field 'Champion.name'
        db.add_column('champions_champion', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, unique=True),
                      keep_default=False)

        # Adding field 'Skin.name'
        db.add_column('champions_skin', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Product._name'
        db.rename_column('champions_product', 'name', '_name')


    models = {
        'accounts.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['champions.Product']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'champions.champion': {
            'Meta': {'object_name': 'Champion', '_ormbases': ['champions.Product']},
            'description': ('django.db.models.fields.TextField', [], {}),
            'detail_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'icon_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '1024'}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['champions.Product']", 'unique': 'True', 'primary_key': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'champions.product': {
            'Meta': {'object_name': 'Product'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'products'", 'symmetrical': 'False', 'through': "orm['accounts.Subscription']", 'to': "orm['auth.User']"})
        },
        'champions.sale': {
            'Meta': {'object_name': 'Sale'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sales'", 'symmetrical': 'False', 'through': "orm['champions.SaleItem']", 'to': "orm['champions.Product']"}),
            'start': ('django.db.models.fields.DateField', [], {})
        },
        'champions.saleitem': {
            'Meta': {'object_name': 'SaleItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '2'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_items'", 'to': "orm['champions.Product']"}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sale_items'", 'to': "orm['champions.Sale']"})
        },
        'champions.skin': {
            'Meta': {'object_name': 'Skin', '_ormbases': ['champions.Product']},
            'champion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['champions.Champion']"}),
            'product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['champions.Product']", 'unique': 'True', 'primary_key': 'True', 'db_column': "'product_ptr_id'"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['champions']
