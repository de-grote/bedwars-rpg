# Bedwars RPG

---

This game is currently in development, don't have high expectations for individual builds.

### Currently, the game includes:

* working collision
* working sneaking, running, and walking
* a (not so nice) scrolling camara
* placeable blocks
* a way to make stages if you know what you're doing (loading in not included)
* customisable controls

#### Things that will be added soon:

* better camara scrolling
* more and better assets (that aren't stolen)

#### Things that will be added later:

* story
* npcs and dialog
* combat (thinking about turn based but haven't made up my mind)
* inventory
* more customisation

---

### Controls:

* A and D to move left and right
* SPACE to jump
* L-CTRL to sprint
* L-SHIFT to sneak
* any click to place block
* Q to reload scene

You can change the controls by changing the values in controls.json.

All keys are case-sensitive.

<details>
<summary>All key names</summary>

| Name         | ASCII | Description
| :----------- | :---- | :----------
| BACKSPACE    | \b    | backspace
| TAB          | \t    | tab
| CLEAR        |       | clear
| RETURN       | \r    | return
| PAUSE        |       | pause
| ESCAPE       |       | escape
| SPACE        |       | space
| EXCLAIM      | !     | exclamation mark
| QUOTEDBL     | "     | double quote
| HASH         | #     | octothorpe
| DOLLAR       | $     | dollar
| AMPERSAND    | &     | ampersand
| QUOTE        | '     | quote
| LEFTPAREN    | (     | left parenthesis
| RIGHTPAREN   | )     | right parenthesis
| ASTERISK     | *     | asterisk
| PLUS         | +     | plus sign
| COMMA        | ,     | comma
| MINUS        | -     | minus sign
| PERIOD       | .     | period
| SLASH        | /     | forward slash
| 0            | 0     | 0
| 1            | 1     | 1
| 2            | 2     | 2
| 3            | 3     | 3
| 4            | 4     | 4
| 5            | 5     | 5
| 6            | 6     | 6
| 7            | 7     | 7
| 8            | 8     | 8
| 9            | 9     | 9
| COLON        | :     | colon
| SEMICOLON    | ;     | semicolon
| LESS         | <     | less-than sign
| EQUALS       | =     | equals sign
| GREATER      | \>    | greater-than sign
| QUESTION     | ?     | question mark
| AT           | @     | at
| LEFTBRACKET  | [     | left bracket
| BACKSLASH    | \     | backslash
| RIGHTBRACKET | ]     | right bracket
| CARET        | ^     | caret
| UNDERSCORE   | _     | underscore
| BACKQUOTE    | `     | grave
| a            | a     | a
| b            | b     | b
| c            | c     | c
| d            | d     | d
| e            | e     | e
| f            | f     | f
| g            | g     | g
| h            | h     | h
| i            | i     | i
| j            | j     | j
| k            | k     | k
| l            | l     | l
| m            | m     | m
| n            | n     | n
| o            | o     | o
| p            | p     | p
| q            | q     | q
| r            | r     | r
| s            | s     | s
| t            | t     | t
| u            | u     | u
| v            | v     | v
| w            | w     | w
| x            | x     | x
| y            | y     | y
| z            | z     | z
| DELETE       |       | delete
| KP0          |       | keypad 0
| KP1          |       | keypad 1
| KP2          |       | keypad 2
| KP3          |       | keypad 3
| KP4          |       | keypad 4
| KP5          |       | keypad 5
| KP6          |       | keypad 6
| KP7          |       | keypad 7
| KP8          |       | keypad 8
| KP9          |       | keypad 9
| KP_PERIOD    | .     | keypad period
| KP_DIVIDE    | /     | keypad divide
| KP_MULTIPLY  | *     | keypad multiply
| KP_MINUS     | -     | keypad minus
| KP_PLUS      | +     | keypad plus
| KP_ENTER     | \r    | keypad enter
| KP_EQUALS    | =     | keypad equals
| UP           |       | up arrow
| DOWN         |       | down arrow
| RIGHT        |       | right arrow
| LEFT         |       | left arrow
| INSERT       |       | insert
| HOME         |       | home
| END          |       | end
| PAGEUP       |       | page up
| PAGEDOWN     |       | page down
| F1           |       | F1
| F2           |       | F2
| F3           |       | F3
| F4           |       | F4
| F5           |       | F5
| F6           |       | F6
| F7           |       | F7
| F8           |       | F8
| F9           |       | F9
| F10          |       | F10
| F11          |       | F11
| F12          |       | F12
| F13          |       | F13
| F14          |       | F14
| F15          |       | F15
| NUMLOCK      |       | numlock
| CAPSLOCK     |       | capslock
| SCROLLOCK    |       | scrollock
| RSHIFT       |       | right shift
| LSHIFT       |       | left shift
| RCTRL        |       | right control
| LCTRL        |       | left control
| RALT         |       | right alt
| LALT         |       | left alt
| RMETA        |       | right meta
| LMETA        |       | left meta
| LSUPER       |       | left Windows key
| RSUPER       |       | right Windows key
| MODE         |       | mode shift
| HELP         |       | help
| PRINT        |       | print screen
| SYSREQ       |       | sysrq
| BREAK        |       | break
| MENU         |       | menu
| POWER        |       | power
| EURO         | €     | Euro
| AC_BACK      |       | Android back button

</details>

---

### Known bugs:

* None

---

### How to run:

Currently, there is no build to just run the game, one will come later.

To run the game, first download the source code.

Make sure you have a python interpreter installed of version 3.10+,

You also need to install pygame by running ``pip install pygame`` into the command line.

If you already have it installed make sure its version 2.0.2+ using ``pip show pygame``,

It may work for pygame 2.0.0+ but no guarantees.

Then lastly you can open main.py using the python interpreter and it'll work!