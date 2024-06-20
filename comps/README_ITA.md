# QCompsLib Framework GUI

Una libreria GUI estremamente potente progettata per massime prestazioni, facilità d'uso e scalabilità, ti permette di costruire facilmente componenti che puoi riutilizzare anche senza dover creare una nuova classe da zero.

## Indice

Caratteristiche della classe foglio di stile [`Style`](#style):

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

Classi stile pronte per l'uso

- [`QSS`](#QSS)
- [`Style(AlignableStyle, Bordered, PaddedStyle, Margined, OpacityEditable, CursorEditable, BackgroundChangeable, FontEditable, FontColorizable, TextEditable, Displayable, Outlined)`](#style)

Gli stili predefiniti possono essere ottenuti da:

- [`TextStyles`](#TextStyles)
- [`PaddingStyles`](#PaddingStyles)
- [`MarginStyles`](#MarginStyles)
- [`OpacityStyles`](#OpacityStyles)
- [`BorderRadiusStyles`](#BorderRadiusStyles)
- [`TabWidgetStyles`](#TabWidgetStyles)
- [`ButtonStyles`](#ButtonStyles)

Classe speciale utilizzata per trovare elementi a cui è stato assegnato un ID (simile a **`getElementByID`** di JavaScript)

- [`Finder`](#Finder)

I componenti possono avere alcune caratteristiche come:

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

Lista dei componenti:

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

### Esplora tutte le classi

---

#### `PropertyOwner`

---

- `properties:Dict[str,Any]`

#### `Displayable`

---
Qualcosa di visualizzabile con una determinata `Style.DisplayPolicy`

- per impostare la politica di visualizzazione puoi usare: `display(v:Style.DisplayPolicy) -> Self`

#### `Outlined`

---
Aggiunge uno stile di contorno

- `outline(outline:str) -> Self`
  
  Imposta lo stile di contorno

#### `AlignableStyle`

---
Aggiunge stile di allineamento

- `alignment(alignment: Style.TextAlignmentPolicy) -> Self`

   Imposta lo stile di allineamento

#### `FontEditable`

---
Aggiunge stili relativi al font

- `fontSize(size: str) -> Self`

  Imposta la dimensione del font

- `fontFamily(family: str) -> Self`

  Imposta il tipo di carattere

#### `FontColorizable`

---
Aggiunge stile di colore del font

- `textColor(color: str) -> Self`

  Imposta il colore del testo

#### `Bordered`

---
Aggiunge stili di bordo

- `border(border: str) -> Self`
- `borderRadius(radius: str) -> Self`

#### `PaddedStyle`

---
Aggiunge stile di padding

- `padding(padding: str) -> Self`

#### `Margined`

---
Aggiunge stile di margine

- `margin(margin: str) -> Self`

#### `TextEditable`

---
Aggiunge stili relativi al testo

- `textShadow(shadow: str) -> Self`
- `wordWrap(wrap: 'Style.WordWrapPolicy') -> Self`
- `letterSpacing(spacing: str) -> Self`
- `wordSpacing(spacing: str) -> Self`
- `textDecoration(decoration: str) -> Self`
- `textAlignment(alignment: 'Style.TextAlignmentPolicy') -> Self`

#### `OpacityEditable`

---
Aggiunge stile di opacità

- `opacity(opacity: str)`

#### `CursorEditable`

---
Aggiunge stile del cursore

- `cursor(cursor: Style.CursorStylePolicy)`

#### `BackgroundChangeable`

---
Aggiunge stile di colore di sfondo

#### `QSS`

---
Classe per la gestione di più fogli di stile

- `set(self, identifier: str, style: 'Style') -> Self`

  Imposta uno stile con un dato identificatore

- `remove(self, identifier: str) -> Self`

  Rimuove uno stile con un dato identificatore

- `to_str(self) -> str`

  Converte il foglio di stile in una rappresentazione stringa, principalmente utilizzata dai parser dei fogli di stile all'interno degli elementi

#### `Style`

---
Classe che rappresenta uno stile con varie opzioni di stile.

La classe `Style` fornisce un insieme completo di opzioni di stile per la personalizzazione. Eredita proprietà da più classi mixin, offrendo funzionalità come allineamento, bordi, padding, margini, opacità, stili di cursore, colori di sfondo, stili relativi al font, colori del testo, opzioni di visualizzazione e contorni.

- **`add(self, qssIdentifier: str, value: str) -> Style`**: Aggiunge una proprietà di stile allo stile.

- **`to_str(self) -> str`**: Converte le proprietà dello stile in una rappresentazione stringa.

- **`merge(self, other: 'Style') -> Style`**: Unisce un altro stile in questo stile, restituendo una nuova istanza.

- **`update(self, other: 'Style') -> Style`**: Aggiorna lo stile con le proprietà di un altro stile.

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
