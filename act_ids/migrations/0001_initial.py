# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActIds'
        db.create_table('act_ids_actids', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('src', self.gf('django.db.models.fields.CharField')(default='index', max_length=6, db_index=True)),
            ('url_exists', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('no_celex', self.gf('django.db.models.fields.CharField')(default=None, max_length=15, null=True, blank=True)),
            ('no_unique_type', self.gf('django.db.models.fields.CharField')(default=None, max_length=4, null=True, blank=True)),
            ('no_unique_annee', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('no_unique_chrono', self.gf('django.db.models.fields.CharField')(default=None, max_length=5, null=True, blank=True)),
            ('propos_origine', self.gf('django.db.models.fields.CharField')(default=None, max_length=4, null=True, blank=True)),
            ('propos_annee', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=4, null=True, blank=True)),
            ('propos_chrono', self.gf('django.db.models.fields.CharField')(default=None, max_length=7, null=True, blank=True)),
            ('dos_id', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=7, null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Act'])),
        ))
        db.send_create_signal('act_ids', ['ActIds'])

        # Adding unique constraint on 'ActIds', fields ['act', 'src']
        db.create_unique('act_ids_actids', ['act_id', 'src'])


    def backwards(self, orm):
        # Removing unique constraint on 'ActIds', fields ['act', 'src']
        db.delete_unique('act_ids_actids', ['act_id', 'src'])

        # Deleting model 'ActIds'
        db.delete_table('act_ids_actids')


    models = {
        'act.act': {
            'Meta': {'unique_together': "(('releve_annee', 'releve_mois', 'no_ordre'),)", 'object_name': 'Act'},
            'adopt_ap_abs': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'adopt_ap_contre': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'adopt_conseil': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'adopt_cs_abs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'adopt_cs_abs'", 'symmetrical': 'False', 'to': "orm['act.Country']"}),
            'adopt_cs_contre': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'adopt_cs_contre'", 'symmetrical': 'False', 'to': "orm['act.Country']"}),
            'adopt_cs_regle_vote': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'adopt_pc_abs': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'adopt_pc_abs'", 'symmetrical': 'False', 'to': "orm['act.Country']"}),
            'adopt_pc_contre': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'adopt_pc_contre'", 'symmetrical': 'False', 'to': "orm['act.Country']"}),
            'adopt_propos_origine': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'amdt_adopt': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'amdt_tabled': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'base_j': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'chgt_base_j': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code_sect_1': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'code_sect_1'", 'null': 'True', 'blank': 'True', 'to': "orm['act.CodeSect']"}),
            'code_sect_2': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'code_sect_2'", 'null': 'True', 'blank': 'True', 'to': "orm['act.CodeSect']"}),
            'code_sect_3': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'code_sect_3'", 'null': 'True', 'blank': 'True', 'to': "orm['act.CodeSect']"}),
            'code_sect_4': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'code_sect_4'", 'null': 'True', 'blank': 'True', 'to': "orm['act.CodeSect']"}),
            'com_amdt_adopt': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'com_amdt_tabled': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'com_proc': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'commission': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cons_b': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'council_a': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'council_path': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'date_doc': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'dde_em': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dg_1': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'dg_1'", 'null': 'True', 'blank': 'True', 'to': "orm['act.DG']"}),
            'dg_2': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'dg_2'", 'null': 'True', 'blank': 'True', 'to': "orm['act.DG']"}),
            'duree_adopt_trans': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'duree_proc_depuis_prop_com': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'duree_proc_depuis_trans_cons': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'duree_tot_depuis_prop_com': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'duree_tot_depuis_trans_cons': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'gvt_compo': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['act.GvtCompo']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modif_propos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nb_lectures': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'nb_point_a': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'nb_point_b': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'no_ordre': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'notes': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'proc_ecrite': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rapp_1': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rapp_1'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'rapp_2': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rapp_2'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'rapp_3': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rapp_3'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'rapp_4': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rapp_4'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'rapp_5': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'rapp_5'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'rejet_conseil': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'releve_annee': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'releve_mois': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'releve_mois_init': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'rep_en_1': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'rep_en_2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'rep_en_3': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'rep_en_4': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'resp_1': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'resp_1'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'resp_2': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'resp_2'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'resp_3': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'resp_3'", 'null': 'True', 'blank': 'True', 'to': "orm['act.Person']"}),
            'sign_pecs': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'split_propos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'suite_2e_lecture_pe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'titre_en': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'titre_rmc': ('django.db.models.fields.CharField', [], {'max_length': '2000'}),
            'transm_council': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_acte': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url_prelex': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1', 'db_index': 'True'}),
            'vote_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'votes_abs_1': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'votes_abs_2': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'votes_agst_1': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'votes_agst_2': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'votes_for_1': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'votes_for_2': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        'act.codeagenda': {
            'Meta': {'object_name': 'CodeAgenda'},
            'code_agenda': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.codesect': {
            'Meta': {'object_name': 'CodeSect'},
            'code_agenda': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.CodeAgenda']", 'null': 'True', 'blank': 'True'}),
            'code_sect': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            'config_cons': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.ConfigCons']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.configcons': {
            'Meta': {'object_name': 'ConfigCons'},
            'config_cons': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.country': {
            'Meta': {'object_name': 'Country'},
            'country': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'})
        },
        'act.dg': {
            'Meta': {'object_name': 'DG'},
            'dg': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'}),
            'dg_nb': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['act.DGNb']", 'symmetrical': 'False'}),
            'dg_sigle': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.DGSigle']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.dgnb': {
            'Meta': {'object_name': 'DGNb'},
            'dg_nb': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.dgsigle': {
            'Meta': {'object_name': 'DGSigle'},
            'dg_sigle': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'act.gvtcompo': {
            'Meta': {'unique_together': "(('start_date', 'end_date'),)", 'object_name': 'GvtCompo'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Country']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['act.Party']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateField', [], {'max_length': '10'})
        },
        'act.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'})
        },
        'act.person': {
            'Meta': {'object_name': 'Person'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.Country']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.Party']", 'null': 'True', 'blank': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'})
        },
        'act_ids.actids': {
            'Meta': {'unique_together': "(('act', 'src'),)", 'object_name': 'ActIds'},
            'act': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Act']"}),
            'dos_id': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_celex': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'no_unique_annee': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'no_unique_chrono': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'no_unique_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'propos_annee': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'propos_chrono': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'propos_origine': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'default': "'index'", 'max_length': '6', 'db_index': 'True'}),
            'url_exists': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['act_ids']