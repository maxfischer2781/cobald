"""
Tools and helpers to declare plugins
"""
from typing import FrozenSet, TypeVar


T = TypeVar("T")


class PluginRequirements:
    """Requirements of a :py:class:`~.SectionPlugin`"""

    __slots__ = "required", "before", "after"

    def __init__(
        self,
        required: bool = False,
        before: FrozenSet[str] = frozenset(),
        after: FrozenSet[str] = frozenset(),
    ):
        self.required = required
        self.before = before
        self.after = after


def constraints(
    *,
    before: FrozenSet[str] = frozenset(),
    after: FrozenSet[str] = frozenset(),
    required: bool = False,
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
            required=required, before=before, after=after
        )
        return plugin

    return section_wrapper