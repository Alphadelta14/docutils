# Authors: David Goodger, Ueli Schlaepfer
# Contact: goodger@users.sourceforge.net
# Revision: $Revision$
# Date: $Date$
# Copyright: This module has been placed in the public domain.

"""
This package contains modules for standard tree transforms available
to Docutils components. Tree transforms serve a variety of purposes:

- To tie up certain syntax-specific "loose ends" that remain after the
  initial parsing of the input plaintext. These transforms are used to
  supplement a limited syntax.

- To automate the internal linking of the document tree (hyperlink
  references, footnote references, etc.).

- To extract useful information from the document tree. These
  transforms may be used to construct (for example) indexes and tables
  of contents.

Each transform is an optional step that a Docutils Reader may choose to
perform on the parsed document, depending on the input context. A Docutils
Reader may also perform Reader-specific transforms before or after performing
these standard transforms.
"""

__docformat__ = 'reStructuredText'


from docutils import languages, ApplicationError, TransformSpec


class TransformError(ApplicationError): pass


class Transform:

    """
    Docutils transform component abstract base class.
    """

    def __init__(self, document, component, startnode=None):
        """
        Initial setup for in-place document transforms.
        """

        self.document = document
        """The document tree to transform."""

        self.component = component
        """The Docutils component running this transform.  Transforms can
        query their controlling components with calls to
        `docutils.Component.supports()`."""

        self.startnode = startnode
        """Node from which to begin the transform.  For many transforms which
        apply to the document as a whole, `startnode` is not set (i.e. its
        value is `None`)."""

        self.language = languages.get_language(document.options.language_code)
        """Language module local to this document."""

    def transform(self):
        """Override to transform the document tree."""
        raise NotImplementedError('subclass must override this method')


class Transformer(TransformSpec):

    """
    The Transformer class records and applies transforms to documents.
    """

    def __init__(self):
        self.transforms = []
        """Queue of transforms to apply."""

        self.applying = None
        """Boolean: am I now applying tranforms?"""

    def add_transform(self, transform_class, priority=None):
        if priority is None:
            priority = transform_class.priority
        self.transforms.append((priority, transform_class, None))
        if self.applying:
            self.transforms.sort()

    def add_transforms(self, transform_list):
        for transform_class in transform_list:
            self.transforms.append((transform_class.priority, transform_class,
                                    None))
        if self.applying:
            self.transforms.sort()

    def add_pending(self, pending, priority=None):
        transform_class = pending.transform
        if priority is None:
            priority = transform_class.priority
        self.transforms.append((priority, transform_class, pending))
        if self.applying:
            self.transforms.sort()
