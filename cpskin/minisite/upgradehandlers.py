# -*- coding: utf-8 -*-


def add_minisite_menu(context):
    context.runImportStepFromProfile('profile-cpskin.ministe:default', 'viewlets')
    context.runImportStepFromProfile('profile-cpskin.ministe:default', 'actions')
