# Joplin Tools

A collection of tools I wrote to help with importing from Trilium notes export. Each tool has a description
at the top of the source code.

# Current Tools

## Node importer

This will create notes using the Joplin API. It can do this for both markdown and other text based files.

This was used to import non markdown files such as .xml .c .h .css etc that the standard Joplin import tool in the
application ignores.
I had these files because Trilium can create different files, eg source code files and then it exports them as such.

This will import these into Joplin and will wrap them in a code block unless its a markdown file.

## Tagger

Trilium was more hierarchical in nature and therefore the exported directory structure was very nested. When it was flattened
using the flatten tool, the notes lost all of their context.

Therefore this is a crude tagging tool that looks at the original export directory (after the replacer has been run)
and builds a list of tags which is just the parent directories of the note excluding the base directory.

For example.

/home/me/notes/export/tech/linux/ubuntu/apt proxy.md

This will get these tags:

- linux
- ubuntu

It will search for the corresponding note in Joplin (using name excluding the extension unless its a markdown file) and
update the tags of the note.

## Flattener

This tool will flatten all files in a directory so every file is under a single top level directory. This was used
to explore using Joplin in the zettelkasten style. 

It will copy the files to a new directory. If you wish to use the tagger tool then leave the original export directory
intact.

It currently excludes the Journal and Trilium Demo directory.

## Replacer

This tool fixes the issues with Joplin not importing images with spaces in the name. This has been tested with an
export from Trilium notes application.

It will rename the image files (or any file with the matching extension).
Then it will look for the file references in the markdown files and update them with the new name.

## Delete All Tags

Simple tool to delete all tags in the Joplin app.

Even deleting tags still leaves them behind if you do a api call to list them.

## Tag Renamer

Utility to rename tags, will find and replace specified characters and update the title accordingly.

# Examples - Import notes from Trilium

Note: There are two directories mentioned here.

```
export_dir_path = The export from Trilium.
output_to_new_dir = The flattened directory of notes.
```

Export the notes from trilium as a markdown directory.

Run the replacer.py tool to remove all spaces from the image files etc.

`python3 preprocessor/replacer.py export_dir_path`

You can now import the notes into Joplin if you want to keep the same hierarchical structure. If you want a flat structure
then carry on.

Run the flattener tool.

`python3 preprocessor/flattener.py export_dir_path output_to_new_dir`

Now import the `output_to_new_dir` into Joplin.

Add tags to the notes based on the previous directory structure.

`python3 postprocessing/tagger.py export_dir_path --token <joplin api token>`

## Missing notes (Source code notes etc that are not markdown files)

Trilium supports adding notes that are source code files etc and these are exported to a non markdown file type. The standard import tool within
Joplin will ignore these. If you want these added then run the next tool. You can pass any file type separated with a space.

`python3 importer/note_importer.py output_to_new_dir --token <joplin api token> --file_types "css xml dat c h"`

Now to add the tags to these.

`python3 postprocessing/tagger.py export_dir_path --token <joplin api token> --file_types "css xml dat c h"`