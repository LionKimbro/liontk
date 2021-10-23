# My Work with Python and Tcl/Tk GUIs
by Lion Kimbro, 2021-10-22  

## <a name="tldr">TLDR</a>

"Too long, didn't read."

* Tcl/Tk is a very powerful way to express GUI concepts.
* I think tkinter gets in the way.
* I wanted to make it easier to use tcl/tk directly from Python, and talk with it.
* Using tkpaint + tcl injection, you can put interactive schematics easily into your GUI.  (For example.)

There are far more ideas in this communication, than just that, but if you need to know something and don't have time to listen to my yarn, let's leave it at that.


## <a name="indices">Indices</a>

* <a name="structure">Structure</a>
	* [TLDR](#tldr) -- read just this, if you're in a rush
	* [The Beginning](#beginning) -- how I got into this mess
	* [Contextualizing GUIs](#context) -- looking at GUIs from afar
	* [Navigating Tcl/Tk](#nav) -- things you need to know about modern Tcl/Tk
	* [Python + Tcl/Tk; Personal History](#history) -- how my work with Python GUIs played out
	* [Tcl/Tk Creative Community](#community) -- when I discovered how great the Tcl/Tk GUI community is
		* [Gub](#gub) -- regular expressions for GUIs!
		* [Tkpaint](#tkpaint) -- directly inject schematics into your code, and manipulate them logically!
	* [Review](#review)
	* [So, liontk](#liontk) --"so these are the forces that led me to create liontk"
	* [Special Note: PySimpleGUI](#pysimplegui) -- consider looking at PySimpleGUI, too
	* [Footnotes](#footnotes) -- I could really use to make more use of these

* <a name="ideas">Notable Ideas</a>
	* [P ∝ M/C](#PMC) -- Power, Meaning, and Clutter
	* [the GUI Triangle: Editor, Memory, and Imperative](#triangle) -- fundamental map of GUI access
	* [CommunityWiki:SchematicMedium](https://communitywiki.org/wiki/SchematicMedium) -- not directly discussed in this paper, but I allude to it frequently

* <a name="references">Project References</a>
	* [HyperCard](https://en.wikipedia.org/wiki/HyperCard) -- an extraordinary technology from the 1990s that nobody seems to know what was so cool about it who didn't directly work with it
	* [TempleOS](https://templeos.org/) -- and somewhere on the Internet, there's an amazing article about the technical wonders found within it
	* [gub](#gub) -- regular expressions for (Tk) GUIs
	* [tkpaint](#tkpaint) -- 1. a "programmer's" diagramming tool; 2. enabling direct injection into Tk's Canvas
	* [PySimpleGUI](#pysimplegui) -- a remarkable GUI system for Python, building on top of tcl/tk
* <a name="articles">Related Articles by me</a>
	* [tkinter Direct Injection](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-18_tkinter-direct.md) -- my initial notes on how to perform direct tcl/tk injection from Python
	* [Lion's Programming Philosophy](https://github.com/LionKimbro/lions_internet_office/blob/main/2021/users/lion/entries/2021-09-06_programming-philosophy.md) -- my programming philosophy, broadly


## <a name="beginning">The Beginning</a>

I started out using tkinter, like so many Python programmers before me, and also dabbled in wx and various other systems.

Nothing ever felt quite right, though -- most things were too complex.  The ratio <a name="PMC">P ∝ M/C,</a> where P is "programming power," M is "meaningful things happening", and C is "mass of code", felt far too low.

I found myself gravitating towards raw tcl/tk.  I realized more and more, "I think tcl/tk is the best raw expression of GUI code."    

## <a name="context">Contextualizing GUIs</a>

Let me contextualize that sentence for a moment:

There's a <a name="triangle">"triangle"</a> I use, when I think about GUIs, based around three points of access to a GUI.  I'll call it "Lion's GUI Triangle."  If somebody somewhere has formalized this concept before, let me know about it -- I love citing things.  But for the time being, here's my conceptualization:

* a GUI as it appears in a GUI editor  -- paradigmatic example: [HyperCard](https://en.wikipedia.org/wiki/HyperCard)
* a GUI as represented in a memory structure  -- consider: an XML file representing a GUI  
* a GUI as constructed by imperative commands  -- consider: executing instructions to build a GUI  
  
I've always wondered, "Is there some kind of form that embodies all three?"  To this day, I have still not found it.  

* **GUI Editor** -- When you work in a GUI builder, there's rarely an easy way to make it so that the GUI can be programmatically assembled.  It'd be nice if you could say, "Note an attachment point here -- ."  It would be also nice if you could just directly draw the GUI into your code, -- that the medium that the code was expressed in, included GUI elements or at least reasonable enough schematic depictions of GUIs, as basic elements.  (For more on this kind of thought, I encourage you to read: [CommunityWiki:SchematicMedium](https://communitywiki.org/wiki/SchematicMedium); consider also the hypertextual medium that HolyC was written in.)  As it is, when you implement a GUI with a GUI editor, you're pretty much stuck with the form that appears in the editor.  
* **In-Memory Structure** -- Now I am thinking about structured representations of GUI -- say, an XML document, perhaps output by a GUI editor -- that represents a GUI.  Now from this angle, you can manipulate the in-memory structure (perhaps XML, JSON, ...,) programmatically, and a GUI builder tool can read it and write to it, and you can programmatically say, "Start this window from this memory structure."  Not bad, but often not so great either:  you have to make a programming layer to produce data structures conveniently.  I think I may want to do further research here, but my memory is that I'm missing a flaw that I encountered when persuing this path.  
* **Imperative Commands** -- And now, we are firmly in the realm that Tcl/Tk finds itself in.  This is where you write lines of code, and the lines of code construct, destroy, or manipulate the state of the GUI environment, and whatever triggers result therein.  Imperative commands can do anything, the only problem is that you have to write them, and they don't look anything like the end product.

(I have, as a life-long side-project, continued to examine GUI systems.  It is easy for me to dream up easy GUI systems.  What's much harder is to write them.  Again, -- and this link goes to exactly the same place: I think [the fundamental problem is the medium](https://communitywiki.org/wiki/SchematicMedium) that we express programs in.  I think that [Terry Davis](https://en.wikipedia.org/wiki/Terry_A._Davis) was on *exactly* the right track about many things technical, and one of those things was in manipulating the fabric that he expressed programs in.)

## <a name="nav">Navigating Tcl/Tk</a>

So the context that I'm looking at tcl/tk in, is from the standpoint of imperative commands.

And here, I have found in Tcl/Tk, what I think is perhaps the nicest way of expressing GUIs.  It genuinely feels gentle, and sensible.

Now here's an important caveat:  Tcl/Tk, on the surface, is a bit of a mess.  There are several decades of cruft, that has built up in it.  But there's also a cure, and that cure is [tkdocs.com, which tells you exactly how to use "the good parts," and ignore all of the other pieces.](https://tkdocs.com/tutorial/intro.html#bestpractices)  For example, there are three systems for placing widgets in Tk, but you only want to focus on one of them: the grid layout manager.  Also, there are old widgets, and the new widgets.  You want to use only the new widgets, save in the special cases where there are only older widgets -- Text, Canvas, and Tree, if I am remembering right.  (And for those, there is nothing really lost.)

## <a name="history">Python + Tcl/Tk; Personal History</a>

However, now there is something of a problem -- Python is an incredible programming language -- how do I work with both Python, and tcl/tk?  To use tkinter is to use what feels like -- a robotic suit around tcl/tk.  The beauty of tcl/tk code is lost, in my opinion, when you use Python's heavily armored, bulky structures, around the svelt and supple tcl/tk code.

Almost ten years ago (today: 2021-10-22), I discovered that it is possible to write directly into tcl.  I remembered that Python has Tcl inside of it for the sake of tkinter, and through experimentation, found a way to access it.  (There's [an email I wrote to the tkinter-discuss mailing list](https://mail.python.org/pipermail/tkinter-discuss/2013-July/003458.html) wherein -- if you look through it -- you can see the example of the difference between Python code, and equivalent tcl/tk code, that I think can show some of the appeal.)

At the time, around 2013 I think, I made a small Python module for accessing Tcl/Tk directly.

And then -- life got in the way, and I worked on other things, and other modes of user-computer interaction, centering primarily on [SDL2](https://www.libsdl.org/).  But then in 2021, (which is now,) while working recently on more sophisticated data systems [("Lion's Entity Package system,")](https://github.com/LionKimbro/entitypackage) I find myself needing a more conventional user interface, for dealing with these data structures.  Ciprian, an inhabitant of my Internet office, made a list of things that we need from a GUI system, and I realized, "Tcl/Tk checks all of these boxes."  So here I am, back again with Tcl/Tk.

## <a name="community">Tcl/Tk Creative Community</a>

And as I have researched Tcl/Tk GUIs and their interaction with Python, I learned something more, too -- The tcl/tk community has been particularly creative, specifically in the area of user interface work.  As I looked through projects on [the tcl wiki,](https://wiki.tcl-lang.org/) I was blown away.

I was particularly impressed with two projects, that I have adopted as primarily influences.
1. [gub](https://wiki.tcl-lang.org/page/Gub)
2. [tkpaint](#tkpaint)

### <a name="gub">Gub</a>

The first project is "Gub," which bills itself as "The World's Fastest GUI Builder."  [(Read about it on the Tcl wiki.)](%28https://wiki.tcl-lang.org/page/Gub%29)  Honestly, it kind of *is.* It *is* the world's fastest GUI builder, I think.

It can take some effort to find the most recent version, and then get it installed, but when you do, -- if you are interested in researching GUI technologies, this is worthwhile -- you can see how quickly you can express ideas in it.  It takes a little training to use, but in the end, you can start expressing things like:

     f t s
      s
    :f0,t0
    |.,f0
    -.,f0

...and getting functional GUIs or bits of GUI out the other end.  It's a little like <a name="guiregex"> *regular expressions for expressing GUIs*,</a> which I think is a worthy idea, all on its own.

Now -- I found the GUI system a little too cryptic for immediate use.  I felt like I was learning a system (gub) within a system (tcl/tk), and those two layers at the same time was a little too difficult.  Also, I am still new to Tcl/Tk, and don't understand it's package ecology.  *Lethally,* I am programming primarily in Python, and I cannot expect users of my programmers to learn the Tcl/Tk package ecology, I am already requiring that potential users perhaps stretch themselves to learn something about Python.  So I do not feel like I can personally build on Gub.  If there were some kind of project in the world to "productize" Gub a bit more -- (the way that, say, regular expressions have been "productized," and made commonplace -- and perhaps Perl 5 Regular Expressions specifically) -- I could see building on it.  But for the time being, it's a beautiful and noteworthy idea.

### <a name="tkpaint">Tkpaint</a>

The second project I found of note is "tkpaint," which is enormously difficult to track down.

You can download [the "only supported version," version 2.0, for Windows 10, (link current 2021-10-22),](https://www.samyzaf.com/tkpaint.zip) from [Samy Zafrany's website.](https://www.samyzaf.com/)  Sadly, this does not seem to (though I haven't exhaustively checked) an executable form of the program.  I also found, somewhere on the Internet, and I may have used the Way Back Machine to locate it, version 1.6 of Samy Zafrany's code, which *is* purely expressed in tcl/tk.  (And thus, you can look at and work with the full source code, and that should work on all operating systems.)

OK, but what's so cool about it?

There are, I think, two primary things that make tkpaint particularly interesting:
1. **It's a "programmer's" diagramming tool.**  I started using it and immediately preferred it over all other schematic editing tools -- except perhaps [my memory of xfig.](#footnote-xfig)  When I want to express a diagram about a part of a program, I find that the "opinions" built into xfig make it very easy to do so: a basic and easy-to-use color palette, a basic snap grid, sensible text defaults, ...  The interface is a little quirky, but it didn't take long to learn and adjust to, and then I fell in love with how easy it was to work the format to rapidly make consistent schematics.
2. **Very crucially: It outputs Tk canvas drawing instructions.**  When you save the document, it can save to tcl code that you can attach directly into a live canvas object!  Because all of the drawing objects and all of the modeling of the drawing objects are 1:1 aligned with the Tk Canvas model, it is a kind of "what you see is what you get" concept.  And the items are all logical tk items.  You can directly manipulate the drawing, and receive events from the drawing, in exactly the same way from code as you can from the drawing program.  If you want to make a schematic representation of some kind of conceptual or real life structure -- perhaps a state machine diagram of the states that code could be in, or if you want to draw the schematic of a house, -- and then treat it in code as a responsive system, you can totally do that, and you can do it easily.  This capacity blew me away, frankly.  For creating "live diagrams," I can't think of any system that works so easily and so accessibly, from a programmer's angle.

But if you're going to *use* that capacity, you're going to need to be in the mind-set of direct tcl/tk code injection.  If you're in the Python tkinter mindset, and not using drops to raw Tcl, you're not going to see that you can do this.  You're going to say, "Well, I have Python code, but that produces Tcl code."

## <a name="review">Review</a>

OK, so, let's take a step back for a moment.

What have I established here?

I've established that:
* GUIs are accessed primarily through three points on a triangle: the GUI editor, the data structure, and through imperative commands.
* Tcl/Tk works primarily through the imperative command.
* Tcl/Tk is great, if you have some modern guidance on how to use it.  Tkdocs.com.
* Gub is an amazing regex system for Tcl/Tk GUIs.
* Tkpaint is (A) a great tool for editing schematics, and (B) can make diagrams directly for Tk canvases, which is amazing.

OK, now what?

## <a name="liontk">So, liontk</a>

Well, I guess:  I started writing GUIs through the mechanisms of Python + Raw Tcl/Tk, and as I worked on some projects, I started formalizing my work a bit, into some typical patterns.

I created this project so that I could share the work that I'm doing here, and some of the fruit of that work.

If you love Python, and if you love GUIs, and if you in particular love Schematics, then I encourage you to play with this and see what it provokes in you.

If you create something with these ideas, I'd love to talk with you, as well.  Presently, (2021-10-22,) I use "Lion's Internet Office" to talk with the world.  [I invite you to learn about it, and meet me there.](https://github.com/LionKimbro/lions_internet_office/)

## <a name="pysimplegui">Special Note: PySimpleGUI</a>

I want to put out a special aside for [PySimpleGUI](https://pysimplegui.readthedocs.io/).  I think that this is a great system for interacting with Python GUIs, and if I weren't such a tinkerer, if I were forbidden from tinkering with my GUI system, then I think that it is PySimpleGUI that would form the basis of my Python GUI programming.  That ratio that I was talking about -- [P ∝ M/C,](#PMC) -- is abundantly present here.

I think that PySimpleGUI needs more love from the Python community, so I am voicing my affirmation of it here.

# Footnotes
<a name="footnote-xfig">#footnote-xfig</a>

I'm having a hard time finding a good free version of x-fig for Windows that doesn't require Cygwin or other complicated steps.  There's [WinFig](http://winfig.com/) (which is proprietary, it seems, and perhaps not exactly xfig,) and there's [the Cygwin + Windows X-Server version](http://transit.iut2.upmf-grenoble.fr/cgi-bin/dwww/usr/share/doc/xfig/html/installation.html#install-xfigwin) (which seems complicated to set up.)

I can't remember -- did xfig support hyperlinks?  Did it support full text search?  I have a persisting dream of a schematic medium that supports full text search across a corpus, and that supports hyperlinks from diagram to diagram.  It genuinely shocks me that -- such a small addition to an editor, and how big an impact it would have -- and yet, how systematically the opportunity has historically been missed.  Why spend years on learning how to build a schematic editor, years refining and perfecting it, and yet not adding a single feature that must take on the order of only hours, days, or at most a couple of weeks, and yet that would dramatically transform the utility, transforming a tool into an entire medium?  [For more on this line, please read CommunityWiki:SchematicMedium.](https://communitywiki.org/wiki/SchematicMedium)
