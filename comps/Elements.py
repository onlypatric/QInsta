# region IMPORTS
from enum import Enum

from attr import attr

from typing import Callable, Dict, List,Any, Self, Tuple, Union, overload, Any
from PyQt6.QtCore import (Qt, QSize, QPoint, QPointF,QRectF, QMargins, QThread,QMimeData)
from PyQt6.QtGui import (QIcon, QAction, QKeyEvent,QFont,QColor, QBrush, QPaintEvent, QPen, QPainter,QDrag,QIntValidator)
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QCheckBox, QLabel,QPushButton, QHBoxLayout, QTextEdit, QLineEdit, QLayout, QTabWidget,QGridLayout, QStackedLayout, QComboBox, QFileDialog, QScrollArea,QDialog, QRadioButton, QSizePolicy, QSlider, QProgressBar,QSpinBox, QDial, QMenuBar, QMenu, QMainWindow, QTableWidget,QTableWidgetItem, QListWidget, QListWidgetItem, QButtonGroup,QGroupBox, QFrame)

from PyQt6.QtCore import pyqtSlot as Slot
# ENDREGION


class PropertyOwner:
    """Something that owns a dictionary of properties
    
    It can be assigned to be a class that holds styles.
    """
    properties: Dict[str, Any]


class Displayable(PropertyOwner):
    """Something displayable with a certain `Style.DisplayPolicy`"""

    def display(self, v: "Style.DisplayPolicy") -> Self:
        """
        Sets the display policy of that stylesheet.
        
        Parameters:
            display (Style.DisplayPolicy): The display policy to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["display"] = v.value
        return self


class Outlined(PropertyOwner):
    """Adds outline style."""

    def outline(self, outline: str) -> Self:
        """
        Sets the outline style.
        
        Parameters:
            outline (str): The outline style to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["outline"] = outline
        return self


class AlignableStyle(PropertyOwner):
    """Adds alignment style."""

    def alignment(self, alignment: "Style.TextAlignmentPolicy") -> Self:
        """
        Sets the alignment style.
        
        Parameters:
            alignment (Style.TextAlignmentPolicy): The alignment policy to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["qproperty-alignment"] = alignment.value
        return self


class FontEditable(PropertyOwner):
    """Adds font-related styles."""

    def fontSize(self, size: str) -> Self:
        """
        Sets the font size.
        
        Parameters:
            size (str): The font size to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["font-size"] = size
        return self

    def fontFamily(self, family: str) -> Self:
        """
        Sets the font family.
        
        Parameters:
            family (str): The font family to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["font-family"] = family
        return self

    def fontWeight(self, style: "Style.FontWeightPolicy") -> Self:
        """
        Sets the font weight.
        
        Parameters:
            style (Style.FontWeightPolicy): The font weight to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        if style == "bold":
            style = Style.FontWeightPolicy.Bold
        elif style == "normal":
            style = Style.FontWeightPolicy.Normal
        elif style == "italic":
            style = Style.FontWeightPolicy.Italic
        self.properties["font-weight"] = style.value
        return self


class FontColorizable(PropertyOwner):
    """Adds font color style."""

    def textColor(self, color: str) -> Self:
        """
        Sets the text color.
        
        Parameters:
            color (str): The color to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["color"] = color
        return self


class Bordered(PropertyOwner):
    """Adds border styles."""

    def border(self, border: str) -> Self:
        """
        Sets the border style.
        
        Parameters:
            border (str): The border style to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["border"] = border
        return self

    def borderRadius(self, radius: str) -> Self:
        """
        Sets the border radius.
        
        Parameters:
            radius (str): The border radius to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["border-radius"] = radius
        return self


class PaddedStyle(PropertyOwner):
    """Adds padding style."""

    def padding(self, padding: str) -> Self:
        """
        Sets the padding.
        
        Parameters:
            padding (str): The padding to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["padding"] = padding
        return self


class Margined(PropertyOwner):
    """Adds margin style."""

    def margin(self, margin: str) -> Self:
        """
        Sets the margin.
        
        Parameters:
            margin (str): The margin to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["margin"] = margin
        return self


class TextEditable(PropertyOwner):
    """Adds text-related styles."""

    def textShadow(self, shadow: str) -> Self:
        """
        Sets the text shadow.
        
        Parameters:
            shadow (str): The text shadow to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["text-shadow"] = shadow
        return self

    def wordWrap(self, wrap: "Style.WordWrapPolicy") -> Self:
        """
        Sets the word wrap policy.
        
        Parameters:
            wrap (Style.WordWrapPolicy): The word wrap policy to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["word-wrap"] = wrap.value
        return self

    def letterSpacing(self, spacing: str) -> Self:
        """
        Sets the letter spacing.
        
        Parameters:
            spacing (str): The letter spacing to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["letter-spacing"] = spacing
        return self

    def wordSpacing(self, spacing: str) -> Self:
        """
        Sets the word spacing.
        
        Parameters:
            spacing (str): The word spacing to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["word-spacing"] = spacing
        return self

    def textDecoration(self, decoration: str) -> Self:
        """
        Sets the text decoration.
        
        Parameters:
            decoration (str): The text decoration to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["text-decoration"] = decoration
        return self

    def textAlignment(self, alignment: "Style.TextAlignmentPolicy") -> Self:
        """
        Sets the text alignment.
        
        Parameters:
            alignment (Style.TextAlignmentPolicy): The text alignment to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["text-align"] = alignment.value
        return self


class OpacityEditable(PropertyOwner):
    """Adds opacity style."""

    def opacity(self, opacity: str) -> Self:
        """
        Sets the opacity.
        
        Parameters:
            opacity (str): The opacity to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["opacity"] = opacity
        return self


class CursorEditable(PropertyOwner):
    """Adds cursor style."""

    def cursor(self, cursor: "Style.CursorStylePolicy") -> Self:
        """
        Sets the cursor style.
        
        Parameters:
            cursor (Style.CursorStylePolicy): The cursor style to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self.properties["cursor"] = cursor.value
        return self


class BackgroundChangeable(PropertyOwner):
    """Adds background color style."""

    def backgroundColor(self, color: str):
        """
        Sets the background color.
        
        Parameters:
            color (str): The background color to be set.
        """
        self.properties["background"] = color
        return self


class QSS:
    """Class for managing stylesheets."""

    def __init__(self) -> None:
        """Initialize an empty stylesheet."""
        self._styles = {}

    def set(self, identifier: str, style: "Style") -> Self:
        """
        Set a style with a given identifier.
        
        Parameters:
            identifier (str): The identifier for the style.
            style (Style): The style to be set.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self._styles[identifier] = style.to_str()
        return self

    def remove(self, identifier: str) -> Self:
        """
        Remove a style with a given identifier.
        
        Parameters:
            identifier (str): The identifier of the style to be removed.
        
        Returns:
            Self: Returns an instance of the class.
        """
        self._styles.pop(identifier)
        return self

    def to_str(self) -> str:
        """
        Convert the stylesheet to a string representation.
        
        Returns:
            str: The string representation of the stylesheet.
        """
        return "; ".join([f"{identifier} {{ {style} }}" for identifier, style in self._styles.items()])

class Style(AlignableStyle, Bordered, PaddedStyle, Margined, OpacityEditable, CursorEditable, BackgroundChangeable, FontEditable, FontColorizable, TextEditable, Displayable, Outlined):
    """Class representing a style with various styling options.

    This class inherits properties from multiple mixin classes to provide a comprehensive
    set of styling options. It includes alignment, border, padding, margin, opacity, cursor,
    background color, font-related styles, text color, text-related styles, display options,
    and outline.

    Attributes:
        properties (Dict[str, str]): A dictionary containing style properties.

    """

    class FontWeightPolicy(Enum):
        """Enumeration of font weight policies."""
        Normal = "normal"
        Italic = "italic"
        Bold = "bold"
        BoldItalic = "bold italic"
        Underline = "underline"
        Overline = "overline"
        StrikeOut = "strikeout"

    class TextAlignmentPolicy(Enum):
        """Enumeration of text alignment policies."""
        Left = "AlignLeft"
        Right = "AlignRight"
        Center = "AlignCenter"
        Justify = "AlignJustify"
        Top = "AlignTop"
        Bottom = "AlignBottom"
        TopLeft = "AlignVCenter"
        TopRight = "AlignHCenter"
        BottomLeft = "AlignBaseline"

    class CursorStylePolicy(Enum):
        """Enumeration of cursor style policies."""
        ArrowCursor = 'arrow'
        UpArrowCursor = 'uparrow'
        CrossCursor = 'cross'
        WaitCursor = 'wait'
        IBeamCursor = 'ibeam'
        SizeVerCursor = 'sizever'
        SizeHorCursor = 'sizehor'
        SizeBDiagCursor = 'sizebdiag'
        SizeFDiagCursor = 'sizefdiag'
        SizeAllCursor = 'sizeall'
        BlankCursor = 'blank'
        SplitVCursor = 'splitv'
        SplitHCursor = 'splith'
        PointingHandCursor = 'pointinghand'
        ForbiddenCursor = 'forbidden'
        OpenHandCursor = 'openhand'
        ClosedHandCursor = 'closedhand'
        WhatsThisCursor = 'whatsthis'
        BusyCursor = 'busy'
        DragMoveCursor = 'dragmove'
        DragCopyCursor = 'dragcopy'
        DragLinkCursor = 'draglink'
        BitmapCursor = 'bitmap'

    class DisplayPolicy(Enum):
        """Enumeration of display policies."""
        None_ = "none"
        Inline = "inline"
        Block = "block"
        InlineBlock = "inline-block"
        Flex = "flex"
        InlineFlex = "inline-flex"
        Grid = "grid"
        InlineGrid = "inline-grid"
        Table = "table"
        TableRow = "table-row"
        TableCell = "table-cell"
        TableColumn = "table-column"
        TableRowGroup = "table-row-group"
        TableColumnGroup = "table-column-group"
        TableCaption = "table-caption"
        Hidden = "hidden"
        InlineHidden = "inline-hidden"
        Visible = "visible"
        InlineVisible = "inline-visible"
        Inherit = "inherit"
        Initial = "initial"
        Unset = "unset"
        Revert = "revert"
        RevertLayer = "revert-layer"
        RevertInline = "revert-inline"
        RevertGroup = "revert-group"
        RevertItem = "revert-item"

    class WordWrapPolicy(Enum):
        """Enumeration of word wrap policies."""
        Enabled = "true"
        Disabled = "false"

    def __init__(self, properties: Dict[str, str] | None = None) -> None:
        """Initialize the Style class with optional initial properties.

        Args:
            properties (Dict[str, str] | None, optional): A dictionary of initial style properties.
                Defaults to None.

        """
        if properties is not None:
            self.properties = properties
        else:
            self.properties = {}

    def add(self, qssIdentifier: str, value: str):
        """Add a style property.

        Args:
            qssIdentifier (str): The identifier of the style property.
            value (str): The value of the style property.

        Returns:
            Style: Returns an instance of the class.

        """
        self.properties[qssIdentifier] = value
        return self

    def to_str(self):
        """Convert the style properties to a string.

        Returns:
            str: A string representation of the style properties.

        """
        content = "\n".join([f"{k}:{v};" for k, v in self.properties.items()])
        return content

    def merge(self, other: "Style") -> "Style":
        """Merge another style into this style.

        Args:
            other (Style): The other style to merge.

        Returns:
            Style: A new instance of the Style class containing the merged style properties.

        """
        copy = self.properties.copy()
        copy.update(other.properties)
        return Style(copy)

    def update(self, other: "Style") -> "Style":
        """Update the style with properties from another style.

        Args:
            other (Style): The other style to update from.

        Returns:
            Style: Returns an instance of the class.

        """
        self.properties.update(other.properties)
        return self


class TextStyles:
    Title = Style().fontSize("40px")\
        .fontWeight(Style.FontWeightPolicy.Bold)
    SubTitle = Style().fontSize("28px")\
        .fontWeight(Style.FontWeightPolicy.Bold)
    TopHeading = Style().fontSize("28px")
    Heading = Style().fontSize("24px")
    SmallHeading = Style().fontSize("20px")
    RedHeading = Style().fontSize("20px").textColor("#e74c3c")
    Body = Style().fontSize("16px")
    Caption = Style().fontSize("14px")
    EndOfPage = StartOfPage = Style().fontSize("13px")
    Label = Style().fontSize("16px").fontWeight(Style.FontWeightPolicy.Bold)
    DarkenedLabel = Style().fontSize("16px").fontWeight(
        Style.FontWeightPolicy.Bold).opacity("0.5")


class PaddingStyles:
    NoPadding = Style().padding("0px")
    Small = Style().padding("5px")
    Medium = Style().padding("10px")
    Large = Style().padding("15px")
    ExtraLarge = Style().padding("20px")


class MarginStyles:
    NoMargin = Style().margin("0px")
    Small = Style().margin("5px")
    Medium = Style().margin("10px")
    Large = Style().margin("15px")
    ExtraLarge = Style().margin("20px")


class OpacityStyles:
    NoOpacity = Style().opacity("0")
    LowOpacity = Style().opacity("0.5")
    MediumOpacity = Style().opacity("0.75")
    HighOpacity = Style().opacity("0.9")
    FullOpacity = Style().opacity("1.0")


class BorderRadiusStyles:
    NoBorderRadius = Style().borderRadius("0px")
    Small = Style().borderRadius("5px")
    Medium = Style().borderRadius("10px")
    Large = Style().borderRadius("15px")
    ExtraLarge = Style().borderRadius("20px")
    Circle = Style().borderRadius("50%")


class TabWidgetStyles:
    clearTab = Style().backgroundColor("transparent").border("0")


class ButtonStyles:
    Primary = QSS().set("Button", Style({
        "background-color": "#4CAF50",
        "border": "none",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#45a049",
    })).set("Button:focus",
            Style({
                "border": "2px solid #4CAF50",
                "outline": "none",
            }))
    Secondary = QSS().set("Button", Style({
        "background-color": "#337ab7",
        "border": "none",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#286090",
    })).set("Button:focus", Style({
        "border": "2px solid #337ab7",
        "outline": "none",
    }))

    Tertiary = QSS().set("Button", Style({
        "background-color": "#f0ad4e",
        "color": "white",
        "padding": "10px 24px",
        "text-align": "center",
        "text-decoration": "none",
        "font-size": "16px",
        "margin": "2px",
        "border-radius": "10px",
    })).set("Button:hover", Style({
        "background-color": "#ec971f",
    })).set("Button:focus", Style({
        "border": "2px solid #f0ad4e",
        "outline": "none",
    }))

    NavPrimary = QSS().set("Button", Style({
        "margin": "2px",
        "padding": "5px",
        "border-radius": "2px",
        "font-size": "16px",
        "color": "white",
        "background-color": "gray",
        "border": "1px solid gray",
    }))


class ButtonGroup(QButtonGroup):
    """Custom ButtonGroup class inheriting from QButtonGroup."""

    # Class variable to store the previous ID
    old_id = ""

    def get(self):
        """Get the ID of the currently checked button in the group.

        Returns:
            int: The ID of the currently checked button.
        """
        return self.checkedId()

    def id(self, name: str) -> Self:
        """Set an ID for the button group and associate it with a name.

        Args:
            name (str): The name to associate with the button group.

        Returns:
            Self: Returns an instance of the class.
        """
        # Remove the old ID from the elements dictionary, if it exists
        if self.old_id != "":
            Finder.elements.pop(self.old_id, None)

        # Add the button group to the elements dictionary with the given name as key
        Finder.elements[name] = self

        # Update the old_id variable with the current name
        self.old_id = name

        return self


class Finder:
    """Class to manage GUI object identification."""

    # Dictionary to store elements with their object names as keys
    elements = {}

    @staticmethod
    def add(element: 'Identifiable|QWidget'):
        """Adds an element to the map.

        Args:
            element (Identifiable|QWidget): The element to add.
                If the element is an instance of Identifiable, its objectName() is used as the key.
                If the element is an instance of QWidget, its objectName() is used as the key.
        """
        Finder.elements[element.objectName()] = element

    @staticmethod
    def remove(element: QWidget | Any | str):
        """Removes an element from the map.

        Args:
            element (QWidget|Any|str): The element to remove.
                If the element is an instance of QWidget, its objectName() is used as the key for removal.
                If the element is a string, it is assumed to be the key for removal.
        """
        if isinstance(element, QWidget):
            Finder.elements.pop(element.objectName(), None)
        else:
            Finder.elements.pop(element, None)

    @staticmethod
    def get(id_: str) -> QWidget | Any:
        """Gets an element from the map.

        Args:
            id_ (str): The key of the element to retrieve.

        Returns:
            QWidget|Any: The element associated with the given key.
        """
        return Finder.elements[id_]

class Alignable:
    """A property class indicating wether a GUI object can be aligned or not"""
    setAlignment: Callable

    def align(self, alignment: Qt.AlignmentFlag) -> Self:
        """Aligns the widget

        Args:
            alignment (Qt.AlignmentFlag): what alignment to apply

        Returns:
            Self: the widget
        """
        self.setAlignment(alignment)
        return self


class Identifiable:
    """Identifiable widget, which supports object naming and widget naming
    """
    objectName: Callable
    setObjectName: Callable
    setAccessibleName: Callable

    def id(self, id_: str) -> Self:
        """Sets the objectName of the widget, replacing the old one if it exists

        Args:
            id_ (str): what to set the objectName to

        Returns:
            Self: the widget
        """
        Finder.remove(self)
        self.setObjectName(id_)
        Finder.add(self)
        return self

    def set_name(self, name: str) -> Self:
        """Sets the accessibleName of the widget, replacing the old one if it exists

        Args:
            name (str): what to set the accessibleName to

        Returns:
            Self: the widget
        """
        self.setAccessibleName(name)
        return self

    def identify(self, name: str | None = None, objectName: str | None = None) -> Self:
        """Identifies the element

        Args:
            name (str, optional): name to apply. Defaults to None.
            objectName (str, optional): objectName to apply. Defaults to None.

        Returns:
            Self: _description_
        """
        if name:
            self.id(name)
        if objectName:
            self.set_name(objectName)
        return self


class TextAttributed:
    """
    Something that can support the editability of a placeholder within itself and the connection of some event handlers such as key press, key release, text changed.
    """
    keyPressEvent: Callable
    keyReleaseEvent: Callable
    textChanged: Any
    setPlaceholderText: Callable

    def key_press(self, event: QKeyEvent) -> Self:
        """
        key press event handler
        """
        self.keyPressEvent(event)
        return self

    def key_release(self, event: QKeyEvent) -> Self:
        """
        key release event handler
        """
        self.keyReleaseEvent(event)
        return self

    def text_changed(self, text: Callable) -> Self:
        """
        text changed event handler
        """
        self.textChanged.connect(text)
        return self

    def set_placeholder(self, text: str) -> Self:
        """
        sets the placeholder text of the widget
        """
        self.setPlaceholderText(text)
        return self


class AnyMenu:
    """A generic menu with common actions"""
    addSeparator: Callable
    addAction: Callable
    addMenu: Callable

    def add_action(self, text: str, triggered_func=None, shortcut: str | None = None) -> Self:
        """Addds an action to a menu

        Args:
            text (str): what the label of that action should be
            triggered_func (Callable, optional): Something that can be called to a `triggered.connect` tunnel. Defaults to None.
            shortcut (str | None, optional): shortcut of the action. Defaults to None.

        Returns:
            Tuple[Self, QAction]: returns itself and the action generated
        """
        action = QAction(text, self)  # type: ignore
        if triggered_func:
            action.triggered.connect(triggered_func)
        if shortcut:
            action.setShortcut(shortcut)
        self.addAction(action)
        return self

    def add_menu(self, menu: "Menu") -> Self:
        """Adds a menu to a menu

        Args:
            menu (Menu): what menu to add

        Returns:
            Tuple[Self, QMenu]: returns itself and the menu generated
        """
        self.addMenu(menu)
        return self

    def add_separator(self) -> Self:
        """Adds a separator to a menu"""
        self.addSeparator()
        return self


class TextEditable:
    """Something that can have editable text"""
    setText: Callable

    def set_text(self, text: str) -> Self:
        """Sets the text of the widget"""
        self.setText(text)
        return self

    def editable(self, editable: bool) -> Self:
        """Sets the text of the widget"""
        self.setReadOnly(not editable)
        return self


class Padded:
    """Class for adding padding and gaps to a widget."""

    setContentsMargins: Callable
    layout_padding: Callable
    content_gap: Callable
    contentsMargins: Callable[[], QMargins]

    def padding(self, p_: int) -> Self:
        """Sets the padding of the widget.

        Args:
            p_ (int): The padding value.

        Returns:
            Self: Returns an instance of the class.
        """
        self.setContentsMargins(p_, p_, p_, p_)
        return self

    def paddingLeft(self, p_: int) -> Self:
        """Sets the left padding of the widget.

        Args:
            p_ (int): The left padding value.

        Returns:
            Self: Returns an instance of the class.
        """
        top = self.contentsMargins().top()
        right = self.contentsMargins().right()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(p_, top, right, bottom)
        return self
    pl = paddingLeft

    def paddingRight(self, p_: int) -> Self:
        """Sets the right padding of the widget.

        Args:
            p_ (int): The right padding value.

        Returns:
            Self: Returns an instance of the class.
        """
        top = self.contentsMargins().top()
        left = self.contentsMargins().left()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(left, top, p_, bottom)
        return self
    pr = paddingRight

    def paddingTop(self, p_: int) -> Self:
        """Sets the top padding of the widget.

        Args:
            p_ (int): The top padding value.

        Returns:
            Self: Returns an instance of the class.
        """
        left = self.contentsMargins().left()
        right = self.contentsMargins().right()
        bottom = self.contentsMargins().bottom()
        self.setContentsMargins(left, p_, right, bottom)
        return self
    pt = paddingTop

    def paddingBottom(self, p_: int) -> Self:
        """Sets the bottom padding of the widget.

        Args:
            p_ (int): The bottom padding value.

        Returns:
            Self: Returns an instance of the class.
        """
        left = self.contentsMargins().left()
        right = self.contentsMargins().right()
        top = self.contentsMargins().top()
        self.setContentsMargins(left, top, right, p_)
        return self
    pb = paddingBottom

    def gap(self, g_: int) -> Self:
        """Sets the gap of the widget.

        Args:
            g_ (int): The gap value.

        Returns:
            Self: Returns an instance of the class.
        """
        try:
            self.setContentsMargins(g_, g_, g_, g_)
            self.layout_padding(g_)
            self.content_gap(g_)
        except:
            pass
        return self
    g = p = gap


class Stylable:
    """Class for adding styles to a widget."""

    setStyleSheet: Callable
    accessibleName: Callable
    objectName: Callable
    styleSheet: Callable
    setAttribute: Callable

    def set_style(self, style: Union[Style, QSS]) -> Self:
        """Sets the style or QSS of the widget.

        Args:
            style (Union[Style, QSS]): The style or QSS to be applied.

        Returns:
            Self: Returns an instance of the class.
        """
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        if isinstance(style, QSS):
            self.setStyleSheet(style.to_str())
        else:
            self.setStyleSheet(f"{self.accessibleName()}{('#'+self.objectName()) if self.objectName() != '' else ''}{{{style.to_str()}}}")
        return self

    def add_style(self, style: Union[Style, QSS]) -> Self:
        """Adds a style or QSS to the widget without replacing the existing one.

        Args:
            style (Union[Style, QSS]): The style or QSS to be added.

        Returns:
            Self: Returns an instance of the class.
        """
        self.setStyleSheet(self.styleSheet() + style.to_str())
        return self

    def add_qss(self, style_sheet: str) -> Self:
        """Adds a raw QSS description to the stylesheet.

        Args:
            style_sheet (str): The stylesheet to apply.

        Returns:
            Self: Returns an instance of the class.
        """
        self.setStyleSheet(self.styleSheet() + style_sheet)
        return self

    def addTo(self, target: str, style: Style) -> Self:
        """Adds a style to a target inside the element itself, such as the pane of a tabwidget.

        Args:
            target (str): The target to apply the style to.
            style (Style): The style to be applied.

        Returns:
            Self: Returns an instance of the class.
        """
        self.setStyleSheet(f"{self.accessibleName()}{('#'+self.objectName()) if self.objectName() != '' else ''}{target}{{{style.to_str()}}}")
        return self

class Attributable:
    """An attributable class used for setting attributes in GUI objects"""
    setAttribute: Callable

    def set_attribute(self, attribute: Qt.WidgetAttribute, value: bool) -> Self:
        """sets an attribute to an element

        Args:
            attribute (Qt.WidgetAttribute)
            value (bool)

        Returns:
            Self: itself
        """
        self.setAttribute(attribute, value)
        return self

class Linked:
    """Special class used to link elements to CheckBoxes, Toggles with the possibility of making it enabled/disabled, visible/notVisible"""
    setEnabled: Callable
    setVisible: Callable

    def link(self, chbox: Union["CheckBox", str]) -> Self:
        """Links the enable state of the object to a CheckBox.

        Args:
            chbox (CheckBox): The CheckBox to link to.

        Returns:
            itself: Returns itself after setting up the linkage.
        """
        if isinstance(chbox, str):
            chbox = Finder.get(chbox)
        self.setEnabled(chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setEnabled(x))
        return self

    def visible(self, chbox: Union["CheckBox", str]):
        """Sets the visibility of the widget to the state of the checkbox"""
        if isinstance(chbox, str):
            chbox = Finder.get(chbox)
        self.setVisible(chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setVisible(x))
        return self

    def notVisible(self, chbox: Union["CheckBox", str]):
        """Sets the visibility of the widget to the state of the checkbox"""
        if isinstance(chbox, str):
            chbox = Finder.get(chbox)
        self.setVisible(not chbox.isChecked())
        chbox.stateChanged.connect(lambda x: self.setVisible(not x))
        return self


class Checkable:
    """A checkable element"""
    setChecked: Callable

    def check(self, checked: bool) -> Self:
        """Sets the checked state of the object.

        Args:
            checked (bool): The desired checked state.

        Returns:
            itself: Returns itself after updating the checked state.
        """
        self.setChecked(checked)
        return self


class Clickable:
    """A clickable element"""
    clicked: Any

    def action(self, action: Callable) -> Self:
        """Connects a QAction to the object's clicked signal.

        Args:
            action (QAction): The QAction to connect.

        Returns:
            itself: Returns itself after connecting the QAction.
        """
        self.clicked.connect(action)
        return self


class Iconizable:
    """An iconizable element"""
    setIcon: Callable

    def set_icon(self, icon: QIcon) -> Self:
        """Sets the icon for the object.

        Args:
            icon (QIcon): The QIcon to set as the object's icon.

        Returns:
            itself: Returns itself after setting the icon.
        """
        self.setIcon(icon)
        return self


class Ranged:
    """An element which might have a range expressed as a integer"""
    setMaximum: Callable
    setMinimum: Callable

    def minV(self, m: int) -> Self:
        """Sets the minimum value for the object.

        Args:
            m (int): The minimum value.

        Returns:
            itself: Returns itself after setting the minimum value.
        """
        self.setMinimum(m)
        return self

    def maxV(self, m: int) -> Self:
        """Sets the maximum value for the object.

        Args:
            m (int): The maximum value.

        Returns:
            itself: Returns itself after setting the maximum value.
        """
        self.setMaximum(m)
        return self


class Sizable:
    """Something which may have a specific size or at least size constraints"""
    setFixedWidth: Callable[[int], None]
    setFixedHeight: Callable[[int], None]
    setMaximumWidth: Callable[[int], None]
    setMaximumHeight: Callable[[int], None]
    setMinimumWidth: Callable[[int], None]
    setMinimumHeight: Callable[[int], None]

    def w(self, w: int) -> Self:
        """Sets the width of the widget"""
        self.setFixedWidth(w)
        return self

    def h(self, h: int) -> Self:
        """Sets the height of the widget"""
        self.setFixedHeight(h)
        return self

    def maxW(self, w: int) -> Self:
        """Sets the maximum width of the widget"""
        self.setMaximumWidth(w)
        return self

    def maxH(self, h: int) -> Self:
        """Sets the maximum height of the widget"""
        self.setMaximumHeight(h)
        return self

    def minW(self, w: int) -> Self:
        """Sets the minimum width of the widget"""
        self.setMinimumWidth(w)
        return self
    
    def minH(self, h: int) -> Self:
        """Sets the minimum height of the widget"""
        self.setMinimumHeight(h)
        return self


class BasicElement(Padded, Stylable, Attributable, Identifiable, Alignable, Sizable):
    """A basic element with simple actions, such as padding, styles, attributes, identification systems, alignments, resizing"""
    setSizePolicy: Callable
    setMinimumSize: Callable
    setMaximumSize: Callable
    setFixedWidth: Callable
    setFixedHeight: Callable
    setEnabled: Callable
    Size = QSizePolicy.Policy
    """
    A basic element that combines functionality from multiple classes.

    Inherited Classes:
    - Padded: Adds padding functionality to the element.
    - Stylable: Provides methods for styling the element with CSS-like styles.
    - Attributable: Allows setting and getting attributes for the element.
    - Identifiable: Adds functionality for assigning and retrieving identifiers for the element.

    Note: This class doesn't define any additional methods but inherits functionality from the mentioned classes.
    """

    def expand(self, wSizePolicy: QSizePolicy.Policy, hSizePolicy: QSizePolicy.Policy) -> Self:
        """Sets the size policy of the element"""
        self.setSizePolicy(wSizePolicy, hSizePolicy)
        return self

    def expandMin(self) -> Self:
        """Sets the size policy of the element"""
        self.setSizePolicy(self.Size.Minimum, self.Size.Minimum)
        return self

    def expandMax(self) -> Self:
        """Sets the size policy of the element"""
        self.setSizePolicy(self.Size.Maximum, self.Size.Maximum)
        return self

    def minSize(self, w: int, h: int) -> Self:
        """Sets the minimum size of the element"""
        self.setMinimumSize(w, h)
        return self

    def maxSize(self, w: int, h: int) -> Self:
        """Sets the maximum size of the element"""
        self.setMaximumSize(w, h)
        return self

    def setW(self, w: int) -> Self:
        """Sets the width of the element"""
        self.setFixedWidth(w)
        return self

    def setH(self, h: int) -> Self:
        """Sets the width of the element"""
        self.setFixedHeight(h)
        return self

    def enabled(self,b:bool) -> Self:
        """sets wether an element shall be visible or not"""
        self.setEnabled(b)
        return self


class Stretch:
    """An element which does not have any properties it is just used to indicate that there must not be a GUI expansion there, essentially allowing for pushing elements upwards, downwards, left or right"""
    pass


Spacer = Stretch


class BaseContainer(QWidget, BasicElement, Linked):
    """
    A base container widget that combines features from QWidget, BasicElement, and Linked.

    Args:
    - items: Optional. Initial items to add to the container. Can be a single widget, a list, or a tuple of widgets, layouts, or stretches.
    - parent: Optional. The parent widget.
    - layout: Optional. The layout to use for the container.
    - style: Optional. The style to apply to the container.

    Methods:
    - __init__: Initializes the BaseContainer with the provided items, parent, layout, and style.
    - add: Overloaded method to add widgets, layouts, or stretches to the container.
    - layout_padding: Sets the padding around the container's layout.
    - content_gap: Sets the gap between items within the container's layout.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, "GroupBox", Tuple, List, Any],
                 parent=None,
                 layout: QLayout | None = None,
                 style: Style | None = None):
        super().__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)
        self.setAccessibleName(self.__class__.__name__)
        self.lyt = layout if layout is not None else QVBoxLayout()
        self.setLayout(self.lyt)
        self.gap(0)
        if style is not None:
            self.set_style(style)
        if items:
            self.add(*items)

    def align(self, alignment: Qt.AlignmentFlag) -> Self:
        """
        Sets the alignment of the container.

        Args:
        - alignment: The alignment to set.

        Returns:
        - itself: Returns itself after setting the alignment.
        """
        self.lyt.setAlignment(alignment)
        return self

    def add(self, *items: Union[QWidget, Tuple, List, str, QLayout, Stretch, Spacer]) -> Self:
        """
        Adds widgets, layouts, or stretches to the container.

        Args:
        - items: Variable number of items to add. Can be QWidget, QLayout, Stretch, or Spacer.

        Returns:
        - itself: Returns the container itself after adding the items.
        """
        for item in items:
            if item is None:
                continue
            elif isinstance(item, QWidget):
                self.lyt.addWidget(item)
            elif isinstance(item, QLayout):
                if isinstance(self.lyt, QHBoxLayout) or isinstance(self.lyt, QVBoxLayout):
                    self.lyt.addLayout(item)
            elif isinstance(item, list):
                self.lyt.addWidget(Horizontal(*item))
            elif isinstance(item, tuple):
                self.lyt.addWidget(Vertical(*item))
            elif isinstance(item, str):
                self.lyt.addWidget(Text(item, Text.Type.P1))
            else:
                if isinstance(self.lyt, QHBoxLayout) or isinstance(self.lyt, QVBoxLayout):
                    self.lyt.addStretch()
        return self

    def remove(self, item: QWidget) -> Self:
        """
        Removes a widget from the container.

        Args:
        - item: The widget to remove.

        Returns:
        - itself: Returns the container itself after removing the widget.
        """
        self.lyt.removeWidget(item)
        return self

    def layout_padding(self, padding: int) -> Self:
        """
        Sets the padding around the container's layout.

        Args:
        - padding: The padding value.

        Returns:
        - itself: Returns the container itself after setting the layout padding.
        """
        self.lyt.setContentsMargins(padding, padding, padding, padding)
        return self

    def content_gap(self, gap: int) -> Self:
        """
        Sets the gap between items within the container's layout.

        Args:
        - gap: The gap value.

        Returns:
        - itself: Returns the container itself after setting the content gap.
        """
        self.lyt.setSpacing(gap)
        return self

class Vertical(BaseContainer):
    """
    A container with a vertical layout.

    Args:
    - items: Variable number of items to add to the vertical container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the vertical container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, Spacer, Tuple, List, "GroupBox", None], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QVBoxLayout(), style=style)


class Horizontal(BaseContainer):
    """
    A container with a horizontal layout.

    Args:
    - items: Variable number of items to add to the horizontal container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the horizontal container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Stretch, Spacer, "GroupBox", Tuple, List, None], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QHBoxLayout(), style=style)


class Grid(BaseContainer):
    """
    A container with a grid layout.

    Args:
    - items: Variable number of items to add to the grid container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the grid container.
    """

    def __init__(self, *items: Union[QWidget, QLayout, Tuple, List], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QGridLayout(), style=style)


class Stacked(BaseContainer):
    """
    A container with a stacked layout.

    Args:
    - items: Variable number of items to add to the stacked container. Can be QWidget, QLayout, Stretch, or Spacer.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the stacked container.
    """
    lyt: QStackedLayout

    def __init__(self, *items: Union[QWidget, QLayout, Tuple, List], parent=None, style: Style | None = None):
        super().__init__(*items, parent=parent, layout=QStackedLayout(), style=style)

    def currentIndex(self, index: int) -> Self:
        """
        Sets the current index of the stacked container.

        Args:
        - index: The index to set.

        Returns:
        - itself: Returns itself after setting the current index.
        """
        self.lyt.setCurrentIndex(index)
        return self

    def currentWidget(self, widget: QWidget) -> Self:
        """
        Sets the current widget of the stacked container.

        Args:
        - widget: The widget to set.

        Returns:
        - itself: Returns itself after setting the current widget.
        """
        self.lyt.setCurrentWidget(widget)
        return self

class Tab:
    """
    Represents a tab within a tab widget.

    Args:
    - tab: The content widget associated with the tab.
    - title: The title of the tab.
    - icon: Optional. The icon associated with the tab.

    Methods:
    - reset: Resets the tab properties to new values.
    - setTab: Sets the content widget for the tab.
    - setTitle: Sets the title of the tab.
    - setIcon: Sets the icon for the tab.
    """

    def __init__(self, tab: QWidget | None = None, title: str | None = None, icon: QIcon | None = None) -> None:
        self.tab = tab
        self.title = title
        self.icon = icon

    def reset(self, tab: QWidget | None = None, title: str | None = None, icon: QIcon | None = None) -> Self:
        """
        Resets the tab properties to new values.

        Args:
        - tab: The content widget associated with the tab.
        - title: The title of the tab.
        - icon: Optional. The icon associated with the tab.

        Returns:
        - itself: Returns itself after resetting the tab properties.
        """
        self.tab = tab
        self.title = title
        self.icon = icon
        return self

    def setTab(self, tab: QWidget) -> Self:
        """
        Sets the content widget for the tab.

        Args:
        - tab: The content widget associated with the tab.

        Returns:
        - itself: Returns itself after setting the tab content widget.
        """
        self.tab = tab
        return self

    def setTitle(self, title: str) -> Self:
        """
        Sets the title of the tab.

        Args:
        - title: The title of the tab.

        Returns:
        - itself: Returns itself after setting the tab title.
        """
        self.title = title
        return self

    def setIcon(self, icon: QIcon) -> Self:
        """
        Sets the icon for the tab.

        Args:
        - icon: The icon associated with the tab.

        Returns:
        - itself: Returns itself after setting the tab icon.
        """
        self.icon = icon
        return self

class Tabs(QTabWidget, BasicElement, Linked, Padded):
    """
    Represents a tab widget.

    Args:
    - elements: Variable number of Tab instances to add to the tab widget.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the tab widget.

    Methods:
    - paneMovable: Sets whether the panes (tabs) are movable.
    - tabIndex: Sets the current tab index.
    - set_tab_close_button: Sets the visibility of close buttons on the tabs.
    - add: Overloaded method to add tabs with different parameters.
    """

    def __init__(self, *elements: Tab, parent: QWidget | None = None, style: Style | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for element in elements:
            self.add(element)

    def paneMovable(self, movable: bool) -> Self:
        """
        Sets whether the panes (tabs) are movable.

        Args:
        - movable: Boolean indicating whether the panes are movable.

        Returns:
        - itself: Returns itself after setting the pane movability.
        """
        self.setMovable(movable)
        return self

    def tabIndex(self, i: int) -> Self:
        """
        Sets the current tab index.

        Args:
        - i: The index of the tab to set as the current tab.

        Returns:
        - itself: Returns itself after setting the current tab index.
        """
        self.setCurrentIndex(i)
        return self

    def tabClosable(self, enabled: bool) -> Self:
        """
        Sets the visibility of close buttons on the tabs.

        Args:
        - enabled: Boolean indicating whether close buttons should be visible.

        Returns:
        - itself: Returns itself after setting the visibility of close buttons.
        """
        self.setTabsClosable(enabled)
        return self

    @overload
    def add(self, tab: Tab) -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str = "") -> Self:
        ...

    @overload
    def add(self, widget: QWidget, title: str = "", icon: QIcon | None = None) -> Self:
        ...

    def add(self, widget: QWidget | Tab, title: str = "", icon: QIcon | None = None) -> Self:  #  type:ignore
        """
        Adds tabs to the tab widget.

        Args:
        - widget: The content widget or Tab instance to add.
        - title: The title of the tab.
        - icon: Optional. The icon associated with the tab.

        Returns:
        - itself: Returns the tab widget itself after adding the tab.
        """
        if isinstance(widget, Tab):
            if widget.icon is not None:
                self.addTab(widget.tab, widget.icon, widget.title)
            else:
                self.addTab(widget.tab, widget.title)
        else:
            if icon is not None:
                self.addTab(widget, icon, title)
            else:
                self.addTab(widget, title)
        return self


class Label(QLabel, BasicElement, Linked, Iconizable):
    """
    Represents a label widget.

    Args:
    - text: The text content of the label.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the label.

    Methods:
    - set_icon: Sets the icon for the label.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setOpenExternalLinks(True)
        self.setWordWrap(True)

    def set(self, text: str) -> Self:
        self.setText(text)
        return self

    def wrap(self, b: bool) -> Self:
        self.setWordWrap(b)
        return self

    def interactiveLinks(self, b: bool) -> Self:
        self.setOpenExternalLinks(b)
        return self

    def icon(self, icon: QIcon) -> Self:
        """
        Sets the icon for the label.

        Args:
        - icon: The QIcon to set as the label's icon.

        Returns:
        - itself: Returns itself after setting the icon.
        """
        self.setPixmap(icon.pixmap(self.size()))
        return self


class Heading(Label):
    """An evolution of Label with the possibility to choose standard text header sizes such as 30px bold,26px bold,22px bold,20px,18px,16px"""
    class Type(Enum):
        """Type of headers which go from H1 to H6"""
        H1 = Style().fontSize("30px").fontWeight(Style.FontWeightPolicy.Bold)
        H2 = Style().fontSize("26px").fontWeight(Style.FontWeightPolicy.Bold)
        H3 = Style().fontSize("22px").fontWeight(Style.FontWeightPolicy.Bold)
        H4 = Style().fontSize("20px").fontWeight(Style.FontWeightPolicy.Normal)
        H5 = Style().fontSize("18px").fontWeight(Style.FontWeightPolicy.Normal)
        H6 = Style().fontSize("16px").fontWeight(Style.FontWeightPolicy.Normal)

    def __init__(self, text: str = "", hp: "Heading.Type" = Type.H1, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(text=text, parent=parent, style=style)
        self.add_style(hp.value)


class Text(Label):
    """An evolution of Label with the possibility to choose standard text paragraph sizes such as 16px, 14px, 12px"""
    class Type(Enum):
        """Type of paragraphs which go from P1 to P3"""
        P1 = Style().fontSize("16px")
        P2 = Style().fontSize("14px")
        P3 = Style().fontSize("12px")

    def __init__(self, text: str = "", hp: "Text.Type" = Type.P1, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(text=text, parent=parent, style=style)
        self.add_style(hp.value)
    def get(self)->str:
        """Returns the text content of the label"""
        return self.text()


class Button(QPushButton, BasicElement, Linked, Clickable, Iconizable):
    """
    Represents a button widget.

    Args:
    - text: The text content of the button.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the button.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class CheckBox(QCheckBox, BasicElement, Checkable, Linked, Iconizable):
    """
    Represents a check box widget.

    Args:
    - text: The text content of the check box.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the check box.
    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)

    def enableCondition(self, other: Union["CheckBox", str]):
        if isinstance(other, str):
            other = Finder.get(other)
        self.setEnabled(other.isChecked())
        # add listener for then other value changes and set the same
        other.stateChanged.connect(lambda x: (self.setChecked(
            other.isChecked()), self.setCheckable(other.isChecked())))
        return self
    def get(self)->bool:
        return self.checkState()==Qt.CheckState.Checked
    def set(self,b:bool)->Self:
        self.setChecked(b)
        return self


class RadioButton(QRadioButton, BasicElement, Checkable, TextEditable, Linked, Iconizable):
    """
    Represents a radio button widget.

    Args:
    - text: The text content of the radio button.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the radio button.

    Methods:
    - group: Adds the radio button to a QButtonGroup.

    """

    def __init__(self, text: str, parent=None, style: Style | None = None):
        super().__init__(text=text, parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
    
    def get(self) -> bool:
        return self.isChecked()
    def set(self, b: bool) -> Self:
        self.setChecked(b)
        return self

    def assign(self, group: QButtonGroup) -> Self:
        """
        Adds the radio button to a QButtonGroup.

        Args:
        - group: The QButtonGroup to add the radio button to.

        Returns:
        - itself: Returns itself after adding to the group.
        """
        group.addButton(self)
        return self

    def check(self, b: bool) -> Self:
        self.setChecked(b)
        return self


class ComboBox(QComboBox, BasicElement, TextEditable, Linked):
    """
    Represents a combo box widget.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the combo box.

    Methods:
    - add: Adds items to the combo box.
    - set: Sets items in the combo box, clearing existing items.
    - clear: Clears all items from the combo box.
    """

    def __init__(self, items: List[str] | Tuple[str], style: Style | None = None):
        super().__init__()
        self.setStyleSheet(style.to_str() if style else "")
        self.add(*items)

    def get(self) -> int:
        """
        Returns the current selected item in the combo box.

        Returns:
        - The current selected item.
        """
        return self.currentIndex()
    
    def getStr(self) -> str:
        """
        Returns the current selected item in the combo box as a string.

        Returns:
        - The current selected item as a string.
        """
        return self.currentText()

    def set(self,s:int):
        """
        Sets the current selected item in the combo box.

        Args:
        - s: The string to set as the current selected item.

        Returns:
        - itself: Returns itself after setting the item.
        """
        self.setCurrentIndex(s)
        return self

    def add(self, *items: str) -> Self:
        """
        Adds items to the combo box.

        Args:
        - items: A list or tuple of strings to add to the combo box.

        Returns:
        - itself: Returns itself after adding items.
        """
        if items:
            for item in items:
                self.addItem(item)
        return self

    def setitems(self, *items: str) -> Self:
        """
        Sets items in the combo box, clearing existing items.

        Args:
        - items: A list or tuple of strings to set in the combo box.

        Returns:
        - itself: Returns itself after setting items.
        """
        self.clear()
        self.add(*items)
        return self

    def clear(self) -> Self:  # type:ignore
        """
        Clears all items from the combo box.

        Returns:
        - itself: Returns itself after clearing items.
        """
        super().clear()
        return self

    def change_listener(self, callback: Callable[[str], None]) -> Self:
        """
        Adds a change listener to the combo box.

        Args:
        - callback: A function to call when the combo box changes.

        Returns:
        - itself: Returns itself after adding the listener.
        """
        self.currentIndexChanged.connect(callback)
        return self


class Field(QLineEdit, BasicElement, TextEditable, Linked, TextAttributed):
    """
    Represents a single-line text input field.

    Args:
    - placeholder: Optional. The placeholder text for the field.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the field.
    """

    def __init__(self, placeholder: str | None = None, parent: QWidget | None = None, style: Style | None = None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        if placeholder:
            self.setPlaceholderText(placeholder)
        self.setAccessibleName(self.__class__.__name__)
        self.hasintvalidator = True

    def set_int(self)->Self:
        """
        Sets the field to accept only integers.

        Returns:
        - itself: Returns itself after setting the field to accept only integers.
        """
        self.setValidator(QIntValidator())
        self.hasintvalidator = True
        return self

    def set(self,v:str):
        """
        Sets the text in the field.

        Args:
        - v: The text to set in the field.

        Returns:
        - itself: Returns itself after setting the text.
        """
        if not isinstance(v,str):
            v=str(v)
        self.setText(v)

    def get(self) -> str:
        """
        Returns the current text in the field.

        Returns:
        - The current text in the field.
        """
        if self.text()=="" and self.hasintvalidator:
            return 0
        if self.hasintvalidator:
            return int(self.text())
        return self.text()


class MultilineField(QTextEdit, BasicElement, TextEditable, Linked, TextAttributed):
    """
    Represents a multi-line text input field.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the field.
    """

    def __init__(self, parent=None, style=None):
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)


class Slider(QSlider, BasicElement, Linked, Ranged):
    """
    Represents a slider widget.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the slider.

    pro tip: its better to use the `ScrollableContainer` which is already custom made with the slider (its a subclass of `Vertical`)
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class ProgressBar(QProgressBar, BasicElement, Linked, Ranged):
    """
    Represents a progress bar widget.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the progress bar.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)


class SpinBox(QSpinBox, BasicElement, Linked, TextEditable, Ranged):
    """
    Represents a spin box widget.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the spin box.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue

    def valueChange(self, fn: Callable) -> Self:
        self.valueChanged.connect(fn)
        return self

    def set_value(self, value: int) -> Self:
        self.setValue(value)
        return self
    
    set = set_value
    
    def get(self) -> int:
        return self.value()


class Dial(QDial, BasicElement, Linked, Ranged):
    """
    Represents a dial widget.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the dial.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setValue


class Action(QAction, BasicElement):
    """
    Represents an action.

    Args:
    - text: The text content of the action.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the action.
    """

    def __init__(self, text: str, f: Callable, key: str | None = None, icon: QIcon | None = None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.triggered.connect(f)
        self.setShortcut(key)
        if icon:
            self.setIcon(icon)


class Separator:
    pass


class Menu(QMenu, AnyMenu):
    """
    Represents a menu.

    Args:
    - title: The title of the menu.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the menu.
    """

    def __init__(self, title: str, *items: Action | Separator, parent=None, style: Style | None = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        for item in items:
            if isinstance(item, Separator):
                self.addSeparator()
                continue
            if isinstance(item, Action):
                self.addAction(item)
                continue
            raise TypeError(f"Invalid item type {type(item)}")


class MenuBar(QMenuBar, AnyMenu):
    """Represents a menu bar."""

    def __init__(self, *items: Menu, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        for item in items:
            self.add_menu(item)


class FileDialog(QFileDialog):
    """
    Represents a file dialog.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the file dialog.
    - mode: Optional. The mode of the file dialog.
    """

    def __init__(self, parent=None, style: Style | None = None, mode: QFileDialog.AcceptMode = QFileDialog.AcceptMode.AcceptOpen):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setAcceptMode(mode)


class Window(QMainWindow, BasicElement,Sizable):
    """
    Represents a main window.

    Args:
    - child: Optional. The central widget of the window.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the window.
    """

    def __init__(self, child: QWidget | Tuple | List | None = None, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        if child:
            if isinstance(child, list):
                child = Horizontal(*child)
            elif isinstance(child, tuple):
                child = Vertical(*child)
            if child is not None:
                self.setCentralWidget(child)

    def set_title(self, title: str) -> Self:
        """
        Sets the title of the window.

        Args:
        - title: The title of the window.

        Returns:
        - itself: Returns itself after setting the title.
        """
        self.setWindowTitle(title)
        return self
    
    

    def set_widget(self, widget: QWidget|List|Tuple) -> Self:
        """
        Sets the central widget of the window.

        Args:
        - widget: The central widget to set.

        Returns:
        - itself: Returns itself after setting the central widget.
        """
        if isinstance(widget, list):
            widget = Horizontal(*widget)
        elif isinstance(widget, tuple):
            widget = Vertical(*widget)
        self.setCentralWidget(widget)
        return self

    @property
    def title(self):
        return self.windowTitle()
    @title.setter
    def title(self, title):
        self.set_title(title)

class Dialog(QDialog, BasicElement, Sizable):
    """
    Represents a dialog.

    Args:
    - child: Optional. The central widget of the dialog.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the dialog.
    """

    def __init__(self, *child: QWidget | Tuple | List | None, parent=None, style: Style | None = None):
        super().__init__(parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.setLayout(QVBoxLayout())
        if child:
            for item in child:
                if isinstance(item, list):
                    item = Horizontal(*item)
                elif isinstance(item, tuple):
                    item = Vertical(*item)
                if item is not None:
                    if isinstance(item, QWidget):
                        self.layout().addWidget(item)
                    elif isinstance(item, QLayout):
                        self.layout().addLayout(item)
                    elif isinstance(item, Spacer):
                        self.layout().addSpacerItem(item)

class ScrollableContainer(Vertical, BasicElement):
    """
    Represents a scrollable container for content.

    Args:
    - content: The content widget to display in the scrollable container.
    - parent: Optional. The parent widget.
    """

    def __init__(self, content: QWidget | Tuple | List, parent=None):
        super().__init__(parent=parent)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Set the content widget for the scroll area
        if isinstance(content, list):
            content = Horizontal(*content)
        elif isinstance(content, tuple):
            content = Vertical(*content)
        self.scroll_area.setWidget(content)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        self.id("scroll-container")
        self.set_style(Style().backgroundColor("transparent"))

        # Set up the main layout
        self.scroll_area.setObjectName("scroll-area")
        self.scroll_area.setStyleSheet(
            "QScrollArea#scroll-area{background-color:transparent}")
        self.add(self.scroll_area)

        # Ensure the content expands to fill the available space
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.gap(0)

    def set_content(self, content: QWidget):
        """
        Sets the content widget for the scrollable container.

        Args:
        - content: The content widget to display in the scrollable container.

        Returns:
        - itself: Returns itself after setting the content.
        """
        self.scroll_area.setWidget(content)
        return self

    def horizontal(self, horizontalBehavior: Qt.ScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn) -> Self:
        self.scroll_area.setHorizontalScrollBarPolicy(horizontalBehavior)
        return self
    h = horizontal

    def vertical(self, verticalBehavior: Qt.ScrollBarPolicy = Qt.ScrollBarPolicy.ScrollBarAlwaysOn) -> Self:
        self.scroll_area.setVerticalScrollBarPolicy(verticalBehavior)
        return self
    v = vertical


class GroupBox(QGroupBox, BasicElement, Padded, Linked):
    layout: Callable[..., QLayout]
    """
    Represents a group box.

    Args:
    - title: The title of the group box.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the group box.
    """

    def __init__(self, content: BaseContainer | Tuple | List, title: str, parent=None, style: Style | None = None):
        super().__init__(title, parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        if isinstance(content, BaseContainer):
            self.setLayout(content.layout())
        elif isinstance(content, tuple):
            l = Vertical(*content)
            self.setLayout(l.layout())
        elif isinstance(content, list):
            l = Horizontal(*content)
            self.setLayout(l.layout())

    def layout_padding(self, p0_: int) -> Self:
        self.layout().setContentsMargins(p0_, p0_, p0_, p0_)
        return self

    def content_gap(self, p0_: int) -> Self:
        self.layout().setSpacing(p0_)
        return self


class Column:
    def __init__(self, head: QTableWidgetItem | str | None = None, *items: QTableWidgetItem | str | QWidget) -> None:
        self.head = head
        self.items = items


class ItemCheckable(QTableWidgetItem):
    def __init__(self, text: str = "") -> None:
        super().__init__()
        self.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                      Qt.ItemFlag.ItemIsEnabled)
        self.setCheckState(Qt.CheckState.Unchecked)
        self.setText(None)

    def get(self) -> bool:
        return self.checkState() == Qt.CheckState.Checked


class Toggle(CheckBox):
    """
    Represents a toggle button.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the toggle button.
    """

    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(self,
                 parent=None,
                 bar_color=Qt.GlobalColor.gray,
                 checked_color="#00B0FF",
                 handle_color=Qt.GlobalColor.white,
                 ):
        super().__init__("")

        self.setMaximumWidth(50)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush = QBrush(bar_color)
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))

        # Setup the rest of the widget.

        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.stateChanged.connect(self._handle_state_change)

    def sizeHint(self):
        return QSize(48, 35)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center().toPointF())
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    def pressed(self, func: Callable[[bool], None]) -> Self:
        self.stateChanged.connect(lambda *x: func(self._handle_position == 1))
        return self
    
    def get(self)->bool:
        return self._handle_position == 1
    def set(self,value:bool):
        self.setChecked(value)
        self.update()

    @Slot(int)
    def _handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    def _get_handle_position(self):
        return self._handle_position

    def handle_position(self, pos):
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we're doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self._handle_position = pos
        self.update()

    def _get_pulse_radius(self):
        return self._pulse_radius

    def _pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()


class Table(QTableWidget, BasicElement, Linked):
    """
    Represents a table widget.

    Args:
    - rows: The initial number of rows in the table.
    - columns: The initial number of columns in the table.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the table.

    Methods:
    - add_row: Adds a new row with the specified data to the table.
    - add_column: Adds a new column with the specified header text and data to the table.
    - set_cell_data: Sets the data for a specific cell in the table.
    - add_button: Adds a button to a specific cell in the table.
    - add_checkbox: Adds a checkbox to a specific cell in the table.
    - add_combobox: Adds a combobox to a specific cell in the table.
    - handle_cell_click: Handles the click event on a cell and executes corresponding actions.
    - set_clicked_function: Sets a function to be called when a cell is clicked.
    """

    def __init__(self, *columns, parent=None, style: Style | None = None) -> None:
        super().__init__(parent=parent)
        self.setStyleSheet(style.to_str() if style else "")
        self.setAccessibleName(self.__class__.__name__)
        self.clicked_function = None
        for column in columns:
            self.add_column(column)

    def add_column(self, column: Column) -> None:
        """
        Adds a new column to the table with the specified header text and data.

        Args:
        - header: The header text for the new column.
        - data: The data for the new column.

        Returns:
        - None: Returns nothing.
        """
        self.setColumnCount(self.columnCount()+1)
        if column.head is not None:
            self.setHorizontalHeaderItem(
                self.columnCount()-1, QTableWidgetItem(column.head))
        for i, data in enumerate(column.items):
            if isinstance(data, str):
                self.setItem(i, self.columnCount()-1, QTableWidgetItem(data))
            elif isinstance(data, QTableWidgetItem):
                self.setItem(i, self.columnCount()-1, data)
            else:
                self.setCellWidget(i, self.columnCount()-1, data)


class LoginForm(Vertical):
    """
    Represents a login form with predefined structure.

    Args:
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the login form.
    """

    def __init__(self, parent=None, style: Style | None = None):
        super().__init__(parent=parent, style=style)
        self.username = Field("Username")
        self.password = Field("Password")

        self.add(
            Label("Login").id("login-header").set_style(Style().add(
                "Label#login-header", "font-size:24px;font-weight:bold")),
            self.username,
            self.password,
            Button("Login").id("login-button"),
            Spacer()
        )

    def get(self) -> Tuple[str, str]:
        """
        Gets the values entered in the login form.

        Returns:
        - Tuple[str, str]: The username and password entered in the form.
        """
        return self.username.get(), self.password.get()


class MultilineAssistedField(Vertical):
    """
    Represents a multiline assisted field with predefined structure.

    Args:
    - denom: The name of the field.
    - importFromFile: Whether to allow importing from a file.
    - suggestions: A list of suggestions to display in the field.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the multiline assisted field.
    """
    def __init__(self, denom: str, importFromFile: bool, suggestions: List[str], identificator: str, parent=None, style: Style | None = None):
        super().__init__(parent=parent, style=style)
        self.textField = MultilineField()
        self.suggestions = ComboBox(
            suggestions).change_listener(self.combobox_listener_call)
        self.set_name("MultilineAssistedField")
        self.id(identificator)
        self.add(
            (
                denom if denom else None,
                self.textField,
                [
                    GroupBox(
                        Vertical(
                            Button("Import "+denom).action(self.load),
                            Button("Export "+denom).action(self.export),
                        ), "File options"
                    ) if importFromFile else None,
                    GroupBox(
                        Vertical(
                            self.suggestions,
                            Button("Add suggestion").action(
                                self.combobox_listener_call)
                        ), "Suggestions"
                    ) if suggestions else None,
                ]
            ),
            Spacer()
        )

    def combobox_listener_call(self, *args, **kwargs):
        self.textField.insertPlainText(self.suggestions.getStr())

    def get(self) -> str:
        return self.textField.toPlainText()
    def set(self, value: str):
        self.textField.setPlainText(value)

    def load(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open file", "", "Text files (*.txt)")
        if path:
            with open(path, "r") as f:
                self.textField.insertPlainText(f.read())

    def export(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save file", "", "Text files (*.txt)")
        if path:
            with open(path, "w") as f:
                f.write(self.textField.toPlainText())


class ListWidget(QListWidget, BasicElement, Linked, Padded):
    """
    Represents a list widget.

    Args:
    - items: The initial items to add to the list.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the list widget.
    """
    def __init__(self, *items: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.addItems(items)

    def add(self, *items: str | QListWidgetItem | None) -> Self:
        if isinstance(items[0], QListWidgetItem):
            for item in items:
                self.addItem(item)  #  type:ignore
            return self
        elif isinstance(items[0],QWidget):
            for item in items:
                i=ListItem()
                self.addItem(i)  #  type:ignore
                self.setItemWidget(i,item)
            return self
        self.addItems(items)  #  type:ignore
        return self

    def change(self, *items: str) -> Self:
        self.clear()
        self.addItems(items)
        return self

    def change_at(self, index: int, item: str) -> Self:
        self.takeItem(index)
        self.insertItem(index, item)
        return self

    def pop(self, index: int) -> str | None:
        item = self.takeItem(index)
        if item:
            return item.text()
        return None

    def remove(self, index: int) -> Self:
        self.takeItem(index)
        return self
    
class ListItem(QListWidgetItem):
    """
    Represents a list item.

    Args:
    - text: The text to display in the list item.
    - parent: Optional. The parent widget.
    """
    def __init__(self, text: str="", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
    def bg(self,bg:str|QColor):
        self.setBackground(QColor(bg))
        return self
    def fg(self, fg:str|QColor):
        self.setForeground(QColor(fg))
        return self
    def fontSize(self,size:int):
        self.setFont(QFont("Arial",size))
        return self

class NavigationLink(Button):
    """
    Represents a navigation link.

    Args:
    - text: The text to display in the navigation link.
    - icon: Optional. The icon to display in the navigation link.
    - dest: Optional. The destination widget to navigate to.
    """
    def __init__(self, text: str, icon: QIcon | None = None, dest: QWidget | None = None):
        super().__init__(text, icon)
        self.dest = dest
        self.id("nav-link")
        self.set_style(Style().add("Button#nav-link", "padding:0px;"))
        self.set_style(ButtonStyles.NavPrimary)

    def target(self, target: QWidget | List | Tuple) -> Self:
        if isinstance(target, List):
            target = Horizontal(*target)
        elif isinstance(target, Tuple):
            target = Vertical(*target)
        self.dest = target
        return self


class NavigationBar(Horizontal, BasicElement):
    """
    Represents a navigation bar.

    Args:
    - items: The initial items to add to the navigation bar.
    - parent: Optional. The parent widget.
    - style: Optional. The style to apply to the navigation bar.
    """
    def __init__(self, *items: NavigationLink | QWidget, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.items = items
        self.set_name("NavigationContainer")
        self.sidebar = Vertical(*items).setW(200)
        self.sidebar.set_name("NavigationSidebar")
        self.sidebar.expand(QSizePolicy.Policy.Expanding,
                            QSizePolicy.Policy.Expanding)
        self.sidebar.align(Qt.AlignmentFlag.AlignTop)
        self.content_bar = Stacked()
        for i, item in enumerate(items):
            if isinstance(item, NavigationLink) and item.dest:
                self.content_bar.add(item.dest)
                item.action(lambda *a, item=item: self.change(item))
            self.sidebar.add(item)
        self.add(self.sidebar, self.content_bar)

    def change(self, item: NavigationLink) -> None:
        if item.dest:
            self.content_bar.currentWidget(item.dest)

    def new(self, *items: NavigationLink | QWidget) -> Self:
        # get the last index in the dictionary self.orders
        for i, item in enumerate(items):
            if isinstance(item, NavigationLink) and item.dest:
                self.content_bar.add(item.dest)
                item.action(lambda *a, item=item: self.change(item))
            self.sidebar.add(item)
        return self

    def shiftAt(self, index: int) -> Self:
        self.change(self.items[index])  # type: ignore
        return self


class Divider(QFrame, BasicElement):
    """
    Represents a divider

    Args:
    - orientation: The orientation of the divider.
    - parent: Optional. The parent widget.
    """
    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Vertical, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.set_name("Divider")
        self.setFrameShape(QFrame.Shape.VLine if orientation ==
                           Qt.Orientation.Vertical else QFrame.Shape.HLine)


class HDivider(Divider):
    """
    Represents a horizontal divider
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)


class VDivider(Divider):
    """
    Represents a vertical divider
    """
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Vertical, parent)