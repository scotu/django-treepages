"""
Template tags for working with lists of model instances which represent
trees.
"""
from django import template
from django.db.models import get_model
from django.db.models.fields import FieldDoesNotExist
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

from mptt.utils import tree_item_iterator, drilldown_tree_for_node

register = template.Library()

class FullDescendantTreeForModelNode(template.Node):
    def __init__(self, model, parent_id, context_var):
        self.model = model
        self.context_var = context_var
        self.parent_id = template.Variable(parent_id)
        #try:
        #    self.parent_id = int(parent_id)
        #except ValueError:
            #TODO: translate error string?
            #raise template.TemplateSyntaxError('full_descendant_tree_for_model tag was given an invalid id (not an integer number)')

    def render(self, context):
        cls = get_model(*self.model.split('.'))
        try:
            actual_parent_id = self.parent_id.resolve(context)
            if cls is None:
                raise template.TemplateSyntaxError(_('full_descendant_tree_for_model tag was given an invalid model: %s') % self.model)
            context[self.context_var] = cls._tree_manager.get(id=actual_parent_id).get_descendants()
            return ''
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError('full_descendant_tree_for_model tag was given an invalid \'%s\' variable (variable does not exist)' % self.parent_id)

def do_full_descendant_tree_for_model(parser, token):
    """
    Populates a template variable with a ``QuerySet`` containing the
    full tree of descendant models for a given ``parent_model_id`` of type ``model``.

    Usage::

       {% full_descendant_tree_for_model [model] [parent_model_id] as [varname] %}

    The model is specified in ``[appname].[modelname]`` format.

    Example::

       {% full_descendant_tree_for_model tests.Genre parent_genre.id as genres %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError(_('%s tag requires four arguments') % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    return FullDescendantTreeForModelNode(bits[1], bits[2], bits[4])

class NavigationDescendantTreeForModelNode(template.Node):
    def __init__(self, model, parent_id, context_var):
        self.model = model
        self.context_var = context_var
        self.parent_id = template.Variable(parent_id)
        #try:
        #    self.parent_id = int(parent_id)
        #except ValueError:
            #TODO: translate error string?
            #raise template.TemplateSyntaxError('full_descendant_tree_for_model tag was given an invalid id (not an integer number)')

    def render(self, context):
        cls = get_model(*self.model.split('.'))
        try:
            actual_parent_id = self.parent_id.resolve(context)
            if cls is None:
                raise template.TemplateSyntaxError(_('navigation_descendant_tree_for_model tag was given an invalid model: %s') % self.model)
            context[self.context_var] = cls._tree_manager.get(id=actual_parent_id).get_descendants().filter(active=True, in_navigation=True)
            return ''
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError('navigation_descendant_tree_for_model tag was given an invalid \'%s\' variable (variable does not exist)' % self.parent_id)

def do_navigation_descendant_tree_for_model(parser, token):
    """
    Populates a template variable with a ``QuerySet`` containing the
    full tree of descendant models for a given ``parent_model_id`` of type ``model``.

    Usage::

       {% full_descendant_tree_for_model [model] [parent_model_id] as [varname] %}

    The model is specified in ``[appname].[modelname]`` format.

    Example::

       {% full_descendant_tree_for_model tests.Genre parent_genre.id as genres %}

    """
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError(_('%s tag requires four arguments') % bits[0])
    if bits[3] != 'as':
        raise template.TemplateSyntaxError(_("second argument to %s tag must be 'as'") % bits[0])
    return NavigationDescendantTreeForModelNode(bits[1], bits[2], bits[4])

register.tag('full_descendant_tree_for_model', do_full_descendant_tree_for_model)
register.tag('navigation_descendant_tree_for_model', do_navigation_descendant_tree_for_model)
