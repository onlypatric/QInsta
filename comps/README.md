# QCompsLib GUI Framework

An extremely powerful GUI library made for maximum performance, ease of use and scalability, you can easily build components which you can reuse even without having to make a new class from scratch

## Table of contents

Traits of stylesheet class [`Style`](#style):

- [`PropertyOwner`](#propertyowner)
- [`Displayable(PropertyOwner)`](#displayable)
- [`Outlined(PropertyOwner)`](#outlined)
- [`AlignableStyle(PropertyOwner)`](#alignablestyle)
- [`FontEditable(PropertyOwner)`](#fonteditable)
- [`FontColorizable(PropertyOwner)`](#fontcolorizable)
- [`Bordered(PropertyOwner)`](#bordered)
- [`PaddedStyle(PropertyOwner)`](#paddedstyle)
- [`Margined(PropertyOwner)`](#margined)
- [`TextEditable(PropertyOwner)`](#texteditable)
- [`OpacityEditable(PropertyOwner)`](#opacityeditable)
- [`CursorEditable(PropertyOwner)`](#cursoreditable)
- [`BackgroundChangeable(PropertyOwner)`](#backgroundchangeable)

Stylesheet classes ready to use

- [`QSS`](#QSS)
- [`Style(AlignableStyle, Bordered, PaddedStyle, Margined, OpacityEditable, CursorEditable, BackgroundChangeable, FontEditable, FontColorizable, TextEditable, Displayable, Outlined)`](#style)

Default premade **static styles** can be obtained from:

- [`TextStyles`](#TextStyles)
- [`PaddingStyles`](#PaddingStyles)
- [`MarginStyles`](#MarginStyles)
- [`OpacityStyles`](#OpacityStyles)
- [`BorderRadiusStyles`](#BorderRadiusStyles)
- [`TabWidgetStyles`](#TabWidgetStyles)
- [`ButtonStyles`](#ButtonStyles)

Special class used to find elements that have been given an id (similar to javascript's **`getElementByID`**)

- [`Finder`](#Finder)

Components may have some traits such as:

- [`Alignable`](#Alignable)
- [`Identifiable`](#Identifiable)
- [`TextAttributed`](#TextAttributed)
- [`TextEditable`](#texteditable)
- [`AnyMenu`](#AnyMenu)
- [`Padded`](#Padded)
- [`Stylable`](#Stylable)
- [`Attributable`](#Attributable)
- [`Linked`](#Linked)
- [`Checkable`](#Checkable)
- [`Clickable`](#Clickable)
- [`Iconizable`](#Iconizable)
- [`Ranged`](#Ranged)
- [`Sizable`](#Sizable)
- [`BasicElement(Padded, Stylable, Attributable, Identifiable, Alignable, Sizable)`](#basicelement)

Component list:

- [`BaseContainer(QWidget, BasicElement, Linked)`](#basecontainer)
- [`Vertical(BaseContainer)`](#vertical)
- [`Horizontal(BaseContainer)`](#horizontal)
- [`Grid(BaseContainer)`](#grid)
- [`Stacked(BaseContainer)`](#stacked)
- [`Tabs(QTabWidget, BasicElement, Linked, Padded)`](#tabs)
- [`Label(QLabel, BasicElement, Linked, Iconizable)`](#label)
- [`Heading(Label)`](#heading)
- [`Text(Label)`](#text)
- [`Button(QPushButton, BasicElement, Linked, Clickable, Iconizable)`](#button)
- [`CheckBox(QCheckBox, BasicElement, Checkable, Linked, Iconizable)`](#checkbox)
- [`RadioButton(QRadioButton, BasicElement, Checkable, TextEditable, Linked, Iconizable)`](#radiobutton)
- [`ComboBox(QComboBox, BasicElement, TextEditable, Linked)`](#combobox)
- [`Field(QLineEdit, BasicElement, TextEditable, Linked, TextAttributed)`](#field)
- [`MultilineField(QTextEdit, BasicElement, TextEditable, Linked, TextAttributed)`](#multilinefield)
- [`Slider(QSlider, BasicElement, Linked, Ranged)`](#slider)
- [`ProgressBar(QProgressBar, BasicElement, Linked, Ranged)`](#progressbar)
- [`SpinBox(QSpinBox, BasicElement, Linked, TextEditable, Ranged)`](#spinbox)
- [`Dial(QDial, BasicElement, Linked, Ranged)`](#dial)
- [`Action(QAction, BasicElement)`](#action)
- [`Menu(QMenu, AnyMenu)`](#menu)
- [`MenuBar(QMenuBar, AnyMenu)`](#menubar)
- [`FileDialog(QFileDialog)`](#filedialog)
- [`Window(QMainWindow, BasicElement,Sizable)`](#window)
- [`Dialog(QDialog, BasicElement, Sizable)`](#dialog)
- [`ScrollableContainer(Vertical, BasicElement)`](#scrollablecontainer)
- [`GroupBox(QGroupBox, BasicElement, Padded, Linked)`](#groupbox)
- [`ItemCheckable(QTableWidgetItem)`](#itemcheckable)
- [`Toggle(CheckBox)`](#toggle)
- [`Table(QTableWidget, BasicElement, Linked)`](#table)
- [`LoginForm(Vertical)`](#loginform)
- [`MultilineAssistedField(Vertical)`](#multilineassistedfield)
- [`ListWidget(QListWidget, BasicElement, Linked, Padded)`](#listwidget)
- [`ListItem(QListWidgetItem)`](#listitem)
- [`NavigationLink(Button)`](#navigationlink)
- [`NavigationBar(Horizontal, BasicElement)`](#navigationbar)
- [`Divider(QFrame, BasicElement)`](#divider)
- [`HDivider(Divider)`](#hdivider)
- [`VDivider(Divider)`](#vdivider)
- [`ButtonGroup(QButtonGroup)`](#buttongroup)

### Explore all the classes

---

#### `PropertyOwner`

---

- `properties:Dict[str,Any]`

#### `Displayable`

---
Something displayable with a certain `Style.DisplayPolicy`

- to set the display policy you can use: `display(v:Style.DisplayPolicy) -> Self`

#### `Outlined`

---
Adds an outline style

- `outline(outline:str) -> Self`
  
  Sets the outline style

#### `AlignableStyle`

---
Adds alignment style

- `alignment(alignment: Style.TextAlignmentPolicy) -> Self`

   Sets the alignment style

#### `FontEditable`

---
Adds font-related styles

- `fontSize(size: str) -> Self`

  Sets the font size

- `fontFamily(family: str) -> Self`

  Sets the font family

#### `FontColorizable`

---
Adds font color style

- `textColor(color: str) -> Self`

  Sets the text color

#### `Bordered`

---
Adds border styles

- `border(border: str) -> Self`
- `borderRadius(radius: str) -> Self`

#### `PaddedStyle`

---
Adds padding style

- `padding(padding: str) -> Self`

#### `Margined`

---
Adds margin style

- `margin(margin: str) -> Self`

#### `TextEditable`

---
Adds text-related styles

- `textShadow(shadow: str) -> Self`
- `wordWrap(wrap: "Style.WordWrapPolicy") -> Self`
- `letterSpacing(spacing: str) -> Self`
- `wordSpacing(spacing: str) -> Self`
- `textDecoration(decoration: str) -> Self`
- `textAlignment(alignment: "Style.TextAlignmentPolicy") -> Self`

#### `OpacityEditable`

---
Adds opacity style

- `def opacity(opacity: str)`

#### `CursorEditable`

---
Adds cursor style

- `cursor(cursor: Style.CursorStylePolicy)`

#### `BackgroundChangeable`

---
Adds background color style

#### `QSS`

---
Class for managing multiple stylesheets

- `set(self, identifier: str, style: "Style") -> Self`

  Sets a style with a given identifier

- `remove(self, identifier: str) -> Self`

  Remove a style with a given identifier

- `def to_str(self) -> str`

  Convert the stylesheet to a string representation, mainly used by stylesheet parsers inside of elements

#### `Style`

### `Style`

Class representing a style with various styling options.

The `Style` class provides a comprehensive set of styling options for customization. It inherits properties from multiple mixin classes, offering features such as alignment, borders, padding, margins, opacity, cursor styles, background colors, font-related styles, text colors, display options, and outlining.

- **`add(self, qssIdentifier: str, value: str) -> Style`**: Add a style property to the style.

- **`to_str(self) -> str`**: Convert the style properties to a string representation.

- **`merge(self, other: "Style") -> Style`**: Merge another style into this style, returning a new instance.

- **`update(self, other: "Style") -> Style`**: Update the style with properties from another style.

#### `FontWeightPolicy`

```python
Normal = "normal"
Italic = "italic"
Bold = "bold"
BoldItalic = "bold italic"
Underline = "underline"
Overline = "overline"
StrikeOut = "strikeout"
```

#### `TextAlignmentPolicy`

```python
Left = "AlignLeft"
Right = "AlignRight"
Center = "AlignCenter"
Justify = "AlignJustify"
Top = "AlignTop"
Bottom = "AlignBottom"
TopLeft = "AlignVCenter"
TopRight = "AlignHCenter"
BottomLeft = "AlignBaseline"
```

#### `CursorStylePolicy`

```python
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
```

#### `DisplayPolicy`

```python
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
```

#### `WordWrapPolicy`

```python
Enabled = "true"
Disabled = "false"
```

#### `ButtonGroup`

#### `BasicElement`

#### `BaseContainer`

#### `Vertical`

#### `Horizontal`

#### `Grid`

#### `Stacked`

#### `Tabs`

#### `Label`

#### `Heading`

#### `Text`

#### `Button`

#### `CheckBox`

#### `RadioButton`

#### `ComboBox`

#### `Field`

#### `MultilineField`

#### `Slider`

#### `ProgressBar`

#### `SpinBox`

#### `Dial`

#### `Action`

#### `Menu`

#### `MenuBar`

#### `FileDialog`

#### `Window`

#### `Dialog`

#### `ScrollableContainer`

#### `GroupBox`

#### `ItemCheckable`

#### `Toggle`

#### `Table`

#### `LoginForm`

#### `MultilineAssistedField`

#### `ListWidget`

#### `ListItem`

#### `NavigationLink`

#### `NavigationBar`

#### `Divider`

#### `HDivider`

#### `VDivider`
