# View Workshop

Demonstration techniques for building views in Django.  This view illustrates all of the
different Shrinking World standard view types.


## Simple Views

The simple views each display a single item in a nicely formatted visual layout.  These views 
all build on a common HTML template. Each of these views can be extended to add extra information
or agragated into a more complex view.


### Template

A Template View is defined by HTML logic in the "templates" directory.  This is loaded using
the template loader.  Page routes define URLs that are tied to views that inherit from the
TemplateView class.

* [HTML Home Page](/views/home)
* [View Inheritance page](/views/page)


### Text

A Text View is for showing the content of a file.  There is no conversion of the file content
as it is display in a "pre" block for preformatted text.

* [Text page](/views/text)


### Document

Documents are implemented through markdown files that come from the filesystem in the "Documents" 
directory.

* [Document page](/views/document)
* [Document Display page](/views/Index.md)
* [Markdown page](/views/markdown)


## Complex Views

Complex views display many different objects within a visual layout.  

Views can be constructed by adding several standard views together.


### Directory

Files are organized into a directory structure.  The Directory View displays a list of the
files in a given directory as a list of hyperlinks.  Clicking on a document link will display
the Document view for the corresponding file.

* [Document Index page](/views/index)


### Card

Card Views display columns of cards.  The content for the page comes from a markdown file.
The doc file is segmented using the "##" markers to define column breaks and the "###" markers
to break the cards.  The remaining file content is display on the cards as HTML.

* [Card Layout page](/views/cards)


### Table

A CSV data block is converted to an HTML table and displayed as the main view.  An optional 
document is used to introduce the table data.

