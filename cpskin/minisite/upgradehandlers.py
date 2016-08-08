# -*- coding: utf-8 -*-


def move_cpskin_actions(context):
    context.runImportStepFromProfile('profile-cpskin.minisite:to0003', 'actions')
    context.runImportStepFromProfile('profile-cpskin.minisite:default', 'actions')


def add_minisite_menu(context):
    context.runImportStepFromProfile('profile-cpskin.minisite:default', 'viewlets')
    context.runImportStepFromProfile('profile-cpskin.minisite:default', 'actions')
