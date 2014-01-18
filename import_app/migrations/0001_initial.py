# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CSVUpload'
        db.create_table('import_app_csvupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('csv_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('import_app', ['CSVUpload'])

        # Adding model 'ImportDosId'
        db.create_table('import_app_importdosid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dos_id', self.gf('django.db.models.fields.IntegerField')(max_length=7)),
            ('no_celex', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('import_app', ['ImportDosId'])

        # Adding unique constraint on 'ImportDosId', fields ['dos_id', 'no_celex']
        db.create_unique('import_app_importdosid', ['dos_id', 'no_celex'])

        # Adding model 'ImportNP'
        db.create_table('import_app_importnp', (
            ('case_nb', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('no_celex', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('np', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('act_type', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('act_date', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('import_app', ['ImportNP'])

        # Adding model 'ImportAdoptPC'
        db.create_table('import_app_importadoptpc', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('releve_annee', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('releve_mois', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('no_ordre', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('adopt_pc_abs', self.gf('django.db.models.fields.CharField')(default=None, max_length=18, null=True, blank=True)),
            ('adopt_pc_contre', self.gf('django.db.models.fields.CharField')(default=None, max_length=18, null=True, blank=True)),
        ))
        db.send_create_signal('import_app', ['ImportAdoptPC'])

        # Adding unique constraint on 'ImportAdoptPC', fields ['releve_annee', 'releve_mois', 'no_ordre']
        db.create_unique('import_app_importadoptpc', ['releve_annee', 'releve_mois', 'no_ordre'])


    def backwards(self, orm):
        # Removing unique constraint on 'ImportAdoptPC', fields ['releve_annee', 'releve_mois', 'no_ordre']
        db.delete_unique('import_app_importadoptpc', ['releve_annee', 'releve_mois', 'no_ordre'])

        # Removing unique constraint on 'ImportDosId', fields ['dos_id', 'no_celex']
        db.delete_unique('import_app_importdosid', ['dos_id', 'no_celex'])

        # Deleting model 'CSVUpload'
        db.delete_table('import_app_csvupload')

        # Deleting model 'ImportDosId'
        db.delete_table('import_app_importdosid')

        # Deleting model 'ImportNP'
        db.delete_table('import_app_importnp')

        # Deleting model 'ImportAdoptPC'
        db.delete_table('import_app_importadoptpc')


    models = {
        'import_app.csvupload': {
            'Meta': {'object_name': 'CSVUpload'},
            'csv_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'import_app.importadoptpc': {
            'Meta': {'unique_together': "(('releve_annee', 'releve_mois', 'no_ordre'),)", 'object_name': 'ImportAdoptPC'},
            'adopt_pc_abs': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'adopt_pc_contre': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_ordre': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'releve_annee': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'releve_mois': ('django.db.models.fields.IntegerField', [], {'max_length': '2'})
        },
        'import_app.importdosid': {
            'Meta': {'unique_together': "(('dos_id', 'no_celex'),)", 'object_name': 'ImportDosId'},
            'dos_id': ('django.db.models.fields.IntegerField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_celex': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'import_app.importnp': {
            'Meta': {'object_name': 'ImportNP'},
            'act_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'act_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'case_nb': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'no_celex': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'np': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['import_app']