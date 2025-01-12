# hotkeys

Simple python application to bundle multiple hotkeys into one

## Run

To run the application, install the requirements using
`pip install -r requirements.txt`

Next, run using
`python -m src`

## Usage

To open the hotkey window, use the hotkey `CTRL + Y`. This will open the window at your current cursor location.

You can add text fragments by typing `add` at the top and pressing enter. Modify hotkeys by typing `edit <name>`, and remove using `remove <name>`.
To insert text into the previous focussed window, type text in the input box, until the desired text is at the top, then press enter. This will close the window and insert the text.