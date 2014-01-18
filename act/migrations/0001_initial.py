# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('act_country', (
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=2, primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('act', ['Country'])

        # Adding model 'Party'
        db.create_table('act_party', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.CharField')(unique=True, max_length=70)),
        ))
        db.send_create_signal('act', ['Party'])

        # Adding model 'PartyFamily'
        db.create_table('act_partyfamily', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Party'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Country'])),
            ('party_family', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('act', ['PartyFamily'])

        # Adding unique constraint on 'PartyFamily', fields ['party', 'country']
        db.create_unique('act_partyfamily', ['party_id', 'country_id'])

        # Adding model 'Person'
        db.create_table('act_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('src', self.gf('django.db.models.fields.CharField')(max_length=4, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['act.Country'], null=True, blank=True)),
            ('party', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['act.Party'], null=True, blank=True)),
        ))
        db.send_create_signal('act', ['Person'])

        # Adding model 'GvtCompo'
        db.create_table('act_gvtcompo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(max_length=10)),
            ('end_date', self.gf('django.db.models.fields.DateField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Country'])),
        ))
        db.send_create_signal('act', ['GvtCompo'])

        # Adding unique constraint on 'GvtCompo', fields ['start_date', 'end_date']
        db.create_unique('act_gvtcompo', ['start_date', 'end_date'])

        # Adding M2M table for field party on 'GvtCompo'
        db.create_table('act_gvtcompo_party', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gvtcompo', models.ForeignKey(orm['act.gvtcompo'], null=False)),
            ('party', models.ForeignKey(orm['act.party'], null=False))
        ))
        db.create_unique('act_gvtcompo_party', ['gvtcompo_id', 'party_id'])

        # Adding model 'DGSigle'
        db.create_table('act_dgsigle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dg_sigle', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
        ))
        db.send_create_signal('act', ['DGSigle'])

        # Adding model 'DGNb'
        db.create_table('act_dgnb', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dg_nb', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
        ))
        db.send_create_signal('act', ['DGNb'])

        # Adding model 'DG'
        db.create_table('act_dg', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dg', self.gf('django.db.models.fields.CharField')(unique=True, max_length=120)),
            ('dg_sigle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.DGSigle'])),
        ))
        db.send_create_signal('act', ['DG'])

        # Adding M2M table for field dg_nb on 'DG'
        db.create_table('act_dg_dg_nb', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dg', models.ForeignKey(orm['act.dg'], null=False)),
            ('dgnb', models.ForeignKey(orm['act.dgnb'], null=False))
        ))
        db.create_unique('act_dg_dg_nb', ['dg_id', 'dgnb_id'])

        # Adding model 'ConfigCons'
        db.create_table('act_configcons', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('config_cons', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('act', ['ConfigCons'])

        # Adding model 'CodeAgenda'
        db.create_table('act_codeagenda', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_agenda', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('act', ['CodeAgenda'])

        # Adding model 'CodeSect'
        db.create_table('act_codesect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_sect', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11)),
            ('config_cons', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['act.ConfigCons'], null=True, blank=True)),
            ('code_agenda', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['act.CodeAgenda'], null=True, blank=True)),
        ))
        db.send_create_signal('act', ['CodeSect'])

        # Adding model 'Act'
        db.create_table('act_act', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('releve_annee', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('releve_mois', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('releve_mois_init', self.gf('django.db.models.fields.CharField')(default=None, max_length=2, null=True, blank=True)),
            ('no_ordre', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('titre_rmc', self.gf('django.db.models.fields.CharField')(max_length=2000)),
            ('council_path', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('titre_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=600, null=True, blank=True)),
            ('code_sect_1', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='code_sect_1', null=True, blank=True, to=orm['act.CodeSect'])),
            ('code_sect_2', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='code_sect_2', null=True, blank=True, to=orm['act.CodeSect'])),
            ('code_sect_3', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='code_sect_3', null=True, blank=True, to=orm['act.CodeSect'])),
            ('code_sect_4', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='code_sect_4', null=True, blank=True, to=orm['act.CodeSect'])),
            ('rep_en_1', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('rep_en_2', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('rep_en_3', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('rep_en_4', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('type_acte', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('base_j', self.gf('django.db.models.fields.CharField')(default=None, max_length=300, null=True, blank=True)),
            ('date_doc', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('commission', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('com_amdt_tabled', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('com_amdt_adopt', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('amdt_tabled', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('amdt_adopt', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_for_1', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_agst_1', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_abs_1', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_for_2', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_agst_2', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('votes_abs_2', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=3, null=True, blank=True)),
            ('rapp_1', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rapp_1', null=True, blank=True, to=orm['act.Person'])),
            ('rapp_2', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rapp_2', null=True, blank=True, to=orm['act.Person'])),
            ('rapp_3', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rapp_3', null=True, blank=True, to=orm['act.Person'])),
            ('rapp_4', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rapp_4', null=True, blank=True, to=orm['act.Person'])),
            ('rapp_5', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='rapp_5', null=True, blank=True, to=orm['act.Person'])),
            ('modif_propos', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nb_lectures', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=1, null=True, blank=True)),
            ('sign_pecs', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('url_prelex', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('adopt_propos_origine', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('com_proc', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('dg_1', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='dg_1', null=True, blank=True, to=orm['act.DG'])),
            ('dg_2', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='dg_2', null=True, blank=True, to=orm['act.DG'])),
            ('resp_1', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='resp_1', null=True, blank=True, to=orm['act.Person'])),
            ('resp_2', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='resp_2', null=True, blank=True, to=orm['act.Person'])),
            ('resp_3', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='resp_3', null=True, blank=True, to=orm['act.Person'])),
            ('transm_council', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('cons_b', self.gf('django.db.models.fields.CharField')(default=None, max_length=500, null=True, blank=True)),
            ('nb_point_b', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=1, null=True, blank=True)),
            ('adopt_conseil', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('nb_point_a', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=1, null=True, blank=True)),
            ('council_a', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('rejet_conseil', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('chgt_base_j', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duree_adopt_trans', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('duree_proc_depuis_prop_com', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('duree_proc_depuis_trans_cons', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('duree_tot_depuis_prop_com', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('duree_tot_depuis_trans_cons', self.gf('django.db.models.fields.IntegerField')(default=None, max_length=5, null=True, blank=True)),
            ('vote_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('adopt_cs_regle_vote', self.gf('django.db.models.fields.CharField')(default=None, max_length=2, null=True, blank=True)),
            ('adopt_ap_contre', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('adopt_ap_abs', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('dde_em', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('split_propos', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('proc_ecrite', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('suite_2e_lecture_pe', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.CharField')(default=None, max_length=2000, null=True, blank=True)),
            ('validated', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1, db_index=True)),
        ))
        db.send_create_signal('act', ['Act'])

        # Adding unique constraint on 'Act', fields ['releve_annee', 'releve_mois', 'no_ordre']
        db.create_unique('act_act', ['releve_annee', 'releve_mois', 'no_ordre'])

        # Adding M2M table for field adopt_cs_contre on 'Act'
        db.create_table('act_act_adopt_cs_contre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('act', models.ForeignKey(orm['act.act'], null=False)),
            ('country', models.ForeignKey(orm['act.country'], null=False))
        ))
        db.create_unique('act_act_adopt_cs_contre', ['act_id', 'country_id'])

        # Adding M2M table for field adopt_cs_abs on 'Act'
        db.create_table('act_act_adopt_cs_abs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('act', models.ForeignKey(orm['act.act'], null=False)),
            ('country', models.ForeignKey(orm['act.country'], null=False))
        ))
        db.create_unique('act_act_adopt_cs_abs', ['act_id', 'country_id'])

        # Adding M2M table for field adopt_pc_contre on 'Act'
        db.create_table('act_act_adopt_pc_contre', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('act', models.ForeignKey(orm['act.act'], null=False)),
            ('country', models.ForeignKey(orm['act.country'], null=False))
        ))
        db.create_unique('act_act_adopt_pc_contre', ['act_id', 'country_id'])

        # Adding M2M table for field adopt_pc_abs on 'Act'
        db.create_table('act_act_adopt_pc_abs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('act', models.ForeignKey(orm['act.act'], null=False)),
            ('country', models.ForeignKey(orm['act.country'], null=False))
        ))
        db.create_unique('act_act_adopt_pc_abs', ['act_id', 'country_id'])

        # Adding M2M table for field gvt_compo on 'Act'
        db.create_table('act_act_gvt_compo', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('act', models.ForeignKey(orm['act.act'], null=False)),
            ('gvtcompo', models.ForeignKey(orm['act.gvtcompo'], null=False))
        ))
        db.create_unique('act_act_gvt_compo', ['act_id', 'gvtcompo_id'])

        # Adding model 'NP'
        db.create_table('act_np', (
            ('case_nb', self.gf('django.db.models.fields.IntegerField')(max_length=10, primary_key=True)),
            ('np', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Country'])),
            ('act_type', self.gf('django.db.models.fields.CharField')(max_length=106)),
            ('act_date', self.gf('django.db.models.fields.DateField')(default=None, max_length=10, null=True, blank=True)),
            ('act', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['act.Act'])),
        ))
        db.send_create_signal('act', ['NP'])


    def backwards(self, orm):
        # Removing unique constraint on 'Act', fields ['releve_annee', 'releve_mois', 'no_ordre']
        db.delete_unique('act_act', ['releve_annee', 'releve_mois', 'no_ordre'])

        # Removing unique constraint on 'GvtCompo', fields ['start_date', 'end_date']
        db.delete_unique('act_gvtcompo', ['start_date', 'end_date'])

        # Removing unique constraint on 'PartyFamily', fields ['party', 'country']
        db.delete_unique('act_partyfamily', ['party_id', 'country_id'])

        # Deleting model 'Country'
        db.delete_table('act_country')

        # Deleting model 'Party'
        db.delete_table('act_party')

        # Deleting model 'PartyFamily'
        db.delete_table('act_partyfamily')

        # Deleting model 'Person'
        db.delete_table('act_person')

        # Deleting model 'GvtCompo'
        db.delete_table('act_gvtcompo')

        # Removing M2M table for field party on 'GvtCompo'
        db.delete_table('act_gvtcompo_party')

        # Deleting model 'DGSigle'
        db.delete_table('act_dgsigle')

        # Deleting model 'DGNb'
        db.delete_table('act_dgnb')

        # Deleting model 'DG'
        db.delete_table('act_dg')

        # Removing M2M table for field dg_nb on 'DG'
        db.delete_table('act_dg_dg_nb')

        # Deleting model 'ConfigCons'
        db.delete_table('act_configcons')

        # Deleting model 'CodeAgenda'
        db.delete_table('act_codeagenda')

        # Deleting model 'CodeSect'
        db.delete_table('act_codesect')

        # Deleting model 'Act'
        db.delete_table('act_act')

        # Removing M2M table for field adopt_cs_contre on 'Act'
        db.delete_table('act_act_adopt_cs_contre')

        # Removing M2M table for field adopt_cs_abs on 'Act'
        db.delete_table('act_act_adopt_cs_abs')

        # Removing M2M table for field adopt_pc_contre on 'Act'
        db.delete_table('act_act_adopt_pc_contre')

        # Removing M2M table for field adopt_pc_abs on 'Act'
        db.delete_table('act_act_adopt_pc_abs')

        # Removing M2M table for field gvt_compo on 'Act'
        db.delete_table('act_act_gvt_compo')

        # Deleting model 'NP'
        db.delete_table('act_np')


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
        'act.np': {
            'Meta': {'object_name': 'NP'},
            'act': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Act']"}),
            'act_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'act_type': ('django.db.models.fields.CharField', [], {'max_length': '106'}),
            'case_nb': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'primary_key': 'True'}),
            'np': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Country']"})
        },
        'act.party': {
            'Meta': {'object_name': 'Party'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '70'})
        },
        'act.partyfamily': {
            'Meta': {'unique_together': "(('party', 'country'),)", 'object_name': 'PartyFamily'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['act.Party']"}),
            'party_family': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'act.person': {
            'Meta': {'object_name': 'Person'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.Country']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['act.Party']", 'null': 'True', 'blank': 'True'}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_index': 'True'})
        }
    }

    complete_apps = ['act']