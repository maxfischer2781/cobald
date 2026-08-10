"""
Tools and helpers to declare plugins
"""

from typing import Iterable, TypeVar, NamedTuple

T = TypeVar("T")


class PluginRequirements(NamedTuple):
    """Requirements of a :py:class:`~.SectionPlugin`"""

    required: bool = False
    before: frozenset[str] = frozenset()
    after: frozenset[str] = frozenset()


def constraints(
    *, before: Iterable[str] = (), after: Iterable[str] = (), required: bool = False
):
    """
    Mark a callable as a plugin with constraints

    :param before: other plugins that must execute before this one
    :param after: other plugins that must execute after this one
    :param required: whether it is an error if the plugin does not apply

    .. note::

        This decorator only sets constraints of a plugin.
        A plugin must still be registered using ``entry_points``.
    """

    def section_wrapper(plugin: T) -> T:
        plugin.__requirements__ = PluginRequirements(
            required=required, before=frozenset(before), after=frozenset(after)
        )
        return plugin

    return section_wrapper


class YAMLTagSettings(NamedTuple):
    """Settings for interpreting a YAML tag"""

    eager: bool = False

    @classmethod
    def fetch(cls, plugin):
        """Provide the settings for `plugin`"""
        try:
            return plugin.__cobald_yaml_tag__
        except AttributeError:
            return cls()

    def mark(self, plugin):
        """Mark `plugin` to use the current settings"""
        plugin.__cobald_yaml_tag__ = self


def yaml_tag(*, eager: bool = False):
    """
    Mark a callable as a YAML tag constructor with specific settings

    :param eager: whether the YAML content must be evaluated eagerly

    Since YAML can express recursive data, nested data structures are evaluated lazily
    by default. This means a constructor receives nested data structures
    (e.g. a ``dict`` of ``dict``s) upfront but nested content is added later on.
    If a constructor requires the entire data at once, set ``eager=True`` to enforce
    eager evaluation before calling the constructor.

    .. note::

        This decorator only serves to apply non-default settings for a plugin.
        A plugin must still be registered using ``entry_points``.
    """

    def mark_settings(plugin: T) -> T:
        YAMLTagSettings(eager=eager).mark(plugin)
        return plugin

    return mark_settings


@yaml_tag(eager=True)
def __yaml_tag_test(*args, **kwargs):
    """YAML tag constructor for testing only"""
    import copy

    return copy.deepcopy(args), copy.deepcopy(kwargs)
