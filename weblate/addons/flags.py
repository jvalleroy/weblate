# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2018 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from weblate.addons.base import BaseAddon
from weblate.addons.events import EVENT_UNIT_PRE_CREATE
from weblate.utils.state import STATE_TRANSLATED, STATE_FUZZY


SUPPORT_FUZZY = frozenset((
    'ts', 'po', 'po-mono', 'po-unwrapped', 'po-mono-unwrapped'
))


class FlagBase(BaseAddon):
    events = (EVENT_UNIT_PRE_CREATE,)
    icon = 'flag'

    @classmethod
    def is_compatible(cls, component):
        if not component.has_template():
            return False
        if component.template_store.format_id in SUPPORT_FUZZY:
            return False
        return super(FlagBase, cls).is_compatible(component)


class SourceEditAddon(FlagBase):
    name = 'weblate.flags.source_edit'
    verbose = _('Flag new source strings to need edit')
    description = _(
        'Whenever a new source string is imported from the VCS, it is '
        'flagged as needing editing in Weblate. This way you can easily '
        'filter and edit source strings written by the developers.'
    )

    def unit_pre_create(self, unit):
        if unit.translation.is_template and unit.state >= STATE_TRANSLATED:
            unit.state = STATE_FUZZY


class TargetEditAddon(FlagBase):
    name = 'weblate.flags.target_edit'
    verbose = _('Flag new translations to need edit')
    description = _(
        'Whenever a new translation unit is imported from the VCS, it is '
        'flagged as needing editing in Weblate. This way you can easily '
        'filter and edit translations created by the developers.'
    )

    def unit_pre_create(self, unit):
        if not unit.translation.is_template and unit.state >= STATE_TRANSLATED:
            unit.state = STATE_FUZZY
