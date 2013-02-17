#!/usr/bin/python

#student id: 42756561
#student name: Shamim Ahmed

from xml.dom import minidom
import os
import codecs

# creates the home page, which displays a list of questions
def create_files(recordlist):
    outputdirname = "output_42756561"
    refdirname = outputdirname + os.sep + "references"
    
    if not os.path.exists(outputdirname):
        os.mkdir(outputdirname)
        
    if not os.path.exists(refdirname):
        os.mkdir(refdirname) 

    result = """
             <html>
             <head>
               <meta http-equiv="Content-type" content="text/html;charset=UTF-8"/>
               <title>Clinical Questions</title>
             </head>
             <body>
               <h1>Clinical Questions</h1>
               <ul>
             """
    
    for record in recordlist:
        id = record.getAttribute("id")
        recordfilename = id + ".html"
        url = record.getElementsByTagName("url").item(0).firstChild.nodeValue
        question = record.getElementsByTagName("question").item(0).firstChild.nodeValue
        answer = record.getElementsByTagName("answer").item(0)
        
        result += "<li>[<a href='%s'>%s</a>] %s [<a href='%s'>source at jfponline</a>]</li>" % (recordfilename, id, question, url)
        
        # create the file containing record info
        create_record_page(id, question, url, answer, outputdirname, recordfilename, refdirname)
                    
    result += """
                </ul>
              </body>
              </html>
              """
              
    homepage = codecs.open(outputdirname + os.sep + "index.html", "w", "utf-8")
    homepage.write(result)
    homepage.close()
    
    
# creates page corresponding to an answer page
def create_record_page(id, question, url, answer, dirname, filename, refdirname):    
    htmlstr = """
              <html>
              <head>
                <meta http-equiv="Content-type" content="text/html;charset=UTF-8"/>
                <title>Question %s</title>
                <style type="text/css">
                  p.snip {
                    font-weight: bold;
                  }
                </style>
              </head>
              <body>
                <h1>Question %s</h1>
                <p>Question : %s [<a href='%s'>Source at jfponline</a>]</p>
              """ % (id, id, question, url)
              
    snipList = answer.getElementsByTagName("snip")
    
    for snip in snipList:
        sniptext = snip.getElementsByTagName("sniptext").item(0).firstChild.nodeValue
        sor = snip.getElementsByTagName("sor").item(0)
        sortype = sor.getAttribute("type")
        sortext = sor.firstChild.nodeValue
        longlist = snip.getElementsByTagName("long")  
        
        htmlstr += "<p class='snip'>%s</p>" % sniptext
        htmlstr += "<p>SOR type: %s, %s</p>" % (sortype, sortext)
        htmlstr += "<ul>"   
        
        for long in longlist:
            longid = long.getAttribute("id")
            longtext = long.getElementsByTagName("longtext").item(0).firstChild.nodeValue
            
            htmlstr += "<li>%s: %s" % (longid, longtext)
            reflist = long.getElementsByTagName("ref")
            
            htmlstr += "<ul>"
            
            # print each reference
            for ref in reflist:
                refid = ref.getAttribute("id")
                infilename = "Abstracts" + os.sep + refid + ".xml"
                outfilename = refdirname + os.sep + refid + ".html"
                outfileaddr = "references" + os.sep + refid + ".html"
                reftext = ref.firstChild.nodeValue
                
                if os.path.exists(infilename):
                    htmlstr += "<li><a href='%s'>%s</a> %s</li>" % (outfileaddr, refid, reftext)
                    create_ref_page(refid, outfilename)
                else:
                    if refid.endswith("NOT_FOUND"):
                        htmlstr += "<li>%s</li>" % (reftext)
                    else:
                        htmlstr += "<li>%s %s</li>" % (refid, reftext)

                           
            htmlstr += "</ul>"
            htmlstr += "</li>"
            
            
        htmlstr += "</ul>"
                  
                
    htmlstr += """
               </body>
               </html>
               """
    
    recordfile = codecs.open(dirname + os.sep + filename, "w", "utf-8")
    recordfile.write(htmlstr)
    recordfile.close()
    

# creates page corresponding to a reference
def create_ref_page(refid, outfilename):
    if os.path.exists(outfilename):
        return
    
    infname = "Abstracts" + os.sep + refid + ".xml"
    infile = open(infname, "r")
    str = infile.read()
    outfile = codecs.open(outfilename, "w", "utf-8")

    xmldoc = minidom.parseString(str)
    root = xmldoc.documentElement
    
    pubmedarticlelist = root.getElementsByTagName("pubmedarticle")
    result = ""
    
    if pubmedarticlelist.length == 1:
        result = get_pubmed_article_info(root)
    else:
        result = get_book_article_info(root)
    
    outfile.write(result)
    outfile.close()
    infile.close()


# returns the markup for an article
def get_pubmed_article_info(docroot):
    pubmedarticle = docroot.getElementsByTagName("pubmedarticle").item(0)
    medlinecitation = pubmedarticle.getElementsByTagName("medlinecitation").item(0)
    article = medlinecitation.getElementsByTagName("article").item(0)
    pmid = medlinecitation.getElementsByTagName("pmid").item(0).firstChild.nodeValue
    
    metadata = get_pubmed_article_metadata(article)
    articletitle = article.getElementsByTagName("articletitle").item(0).firstChild.nodeValue
    authors = get_pubmed_article_authors(article)
    affiliation = get_pubmed_article_affiliation(article)
    abstract = get_pubmed_article_abstract(article)
    corrections = get_pubmed_article_commentcorrections(medlinecitation)
    publicationtypes = get_pubmed_article_publicationtypes(article)
    meshheadings = get_pubmed_article_meshterms(medlinecitation)
        
    htmlstr = """
              <html>
              <head>
                <meta http-equiv="Content-type" content="text/html;charset=UTF-8"/>
                <title>%s</title>
                <style type="text/css">
                  h1 {
                    margin-top: 15px;
                    margin-bottom: 5px;
                    font-size: 24px;
                  }
                  
                  h3 {
                    margin-bottom: 5px;
                    font-size: 18px;
                  }
                  
                  h4 {
                    margin-bottom: 5px;
                  }
                  
                  span.label {
                    font-weight: bold;
                    font-size: 12px;
                  }
                  
                  p.first {
                    margin-top: 5px;
                  }
                </style>
              </head>
              <body>
                <div class='metadata'>%s</div>
                <h1>%s</h1>
                """ % (articletitle, metadata, articletitle)
                
    if authors != "":
        htmlstr += "<div class='authors'>%s</div>" % authors
        
    if affiliation != "":
        htmlstr += "<div class='affiliation'>%s</div>" % affiliation
        
    if corrections != "":
        htmlstr += "<h4>Erratum in</h4>"
        htmlstr += "<div class='corrections'>%s</div>" % corrections
        
    if abstract != "":
        htmlstr += "<h3>Abstract</h3>"
        htmlstr += "<div class='abstract'>%s</div>" % abstract
        
    htmlstr += """
               <h3>PMID</h3>
               <div class='pmid'>%s [PubMed - indexed for MEDLINE]</div>
               """ % pmid
    
    if publicationtypes != "":
        htmlstr += "<h3>Publication Types</h3>"
        htmlstr += "<div class='publication-types'>%s</div>" % publicationtypes
        
    if meshheadings != "":
        htmlstr += "<h3>MeSH Terms</h3>"
        htmlstr += "<div class='mesh-items'>%s</div>" % meshheadings
        
                
    htmlstr += """
               </body>
               </html>
               """
              
    return htmlstr


# returns list of authors for an article
def get_pubmed_article_authors(article):
    authorlist = article.getElementsByTagName("authorlist")
    authorstr = ""
    
    if authorlist.length > 0:
        authors = authorlist.item(0).getElementsByTagName("author")
        
        for author in authors:            
            name = ""
            lastname = ""
            initials = ""
            
            # sometimes the author is represented by a collective name, so we need to check for it
            collectivename = author.getElementsByTagName("collectivename")

            
            if collectivename.length > 0:
                name = collectivename.item(0).firstChild.nodeValue
            else:
                lastname = author.getElementsByTagName("lastname").item(0).firstChild.nodeValue    
                initialslist = author.getElementsByTagName("initials")
                
                if initialslist.length > 0:
                    initials = initialslist.item(0).firstChild.nodeValue
                
            if name != "":
                authorstr += name + ", "
            else:
                if initials == "": 
                    authorstr +=  lastname + ", "
                else:
                    authorstr +=  lastname + " " + initials + ", "
    
    if authorstr == "":
        return authorstr
    else:
        return authorstr[:(len(authorstr) - 2)]


# returns affiliation of authors    
def get_pubmed_article_affiliation(article):
    str = ""
    
    afflist = article.getElementsByTagName("affiliation")
    
    if afflist.length > 0:
        str = afflist.item(0).firstChild.nodeValue
    
    return str


#returns abstract for an article
def get_pubmed_article_abstract(article):
    str = ""
    
    abstractlist = article.getElementsByTagName("abstract")
    
    if abstractlist.length > 0:
        abstract = abstractlist.item(0)
        abstxtlist = abstract.getElementsByTagName("abstracttext")
        
        if abstxtlist.length == 1:
            abstxt = abstxtlist.item(0).firstChild.nodeValue
            str += "<p class='first'>" + abstxt + "</p>"
        elif abstxtlist.length > 1:
            cnt = 0
            for abstxt in abstxtlist:
                label = abstxt.getAttribute("label")
                txt = abstxt.firstChild.nodeValue     
                
                if cnt == 0:
                    str += "<p class='first'>"
                else:
                    str += "<p>"
                               
                str += "<span class='label'>%s:</span>%s</p>" % (label, txt)
                cnt = cnt + 1

    return str


# returns metadata (journal issue etc) for an article
def get_pubmed_article_metadata(article):
    str = ""
    journal = article.getElementsByTagName("journal").item(0)
    journaltitle = journal.getElementsByTagName("title").item(0).firstChild.nodeValue
    str += "%s. " % journaltitle.strip()
    
    journalissue = journal.getElementsByTagName("journalissue").item(0)
    date = get_pubmed_article_date(journalissue)
    str += "%s;" % date.strip()
    
    volume = ""
    issue = ""
    
    volumelist = journalissue.getElementsByTagName("volume")
    
    if volumelist.length > 0:
        volume = volumelist.item(0).firstChild.nodeValue
        
    if volume != "":
        str += volume.strip()
        
    issuelist = journalissue.getElementsByTagName("issue")
    
    if issuelist.length > 0:
        issue = issuelist.item(0).firstChild.nodeValue
        
    if issue != "":
        str += "(%s)" % issue.strip()
    
        
    pagination = get_pubmed_article_pagination(article)
    str += ":%s." % pagination.strip()
            
    return str


# returns correction info for an article
def get_pubmed_article_commentcorrections(medlinecitation):
    str = ""
    correctionslist = medlinecitation.getElementsByTagName("commentscorrectionslist")
    
    if correctionslist.length > 0:
        corrections = correctionslist.item(0).getElementsByTagName("commentscorrections")
        
        for corr in corrections:
            str += corr.getElementsByTagName("refsource").item(0).firstChild.nodeValue
            str += "<br/>"
                        
    return str


# returns publication types for an article
def get_pubmed_article_publicationtypes(article):
    str = ""
    publicationtypelist = article.getElementsByTagName("publicationtypelist")
    
    if publicationtypelist.length > 0:
        publicationtypes = publicationtypelist.item(0).getElementsByTagName("publicationtype")
        
        for pubtype in publicationtypes:
            str += pubtype.firstChild.nodeValue + "<br/>"
                
    return str


# return mesh terms for an article
def get_pubmed_article_meshterms(medlinecitation):
    str = ""
    
    meshheadinglist = medlinecitation.getElementsByTagName("meshheadinglist")
    
    if meshheadinglist.length > 0:
        meshheadings = meshheadinglist.item(0).getElementsByTagName("meshheading")
                
        for mheading in meshheadings:
            descriptorname = mheading.getElementsByTagName("descriptorname").item(0)
            str += descriptorname.firstChild.nodeValue
            descmajortopic = descriptorname.getAttribute("majortopicyn").lower()

            if descmajortopic == "y":
                 str += "*"
                
            qualifiernamelist = mheading.getElementsByTagName("qualifiername")
            
            for qualifiername in qualifiernamelist:  
                str += "/" + qualifiername.firstChild.nodeValue
                qualmajortopic = qualifiername.getAttribute("majortopicyn").lower()
                                
                if qualmajortopic == "y":
                     str += "*"
                                      
            str += "<br/>"
         
    return str


# retrieve page numbers for an article
def get_pubmed_article_pagination(article):
    paginationlist = article.getElementsByTagName("pagination")
    
    if paginationlist.length == 0:
        medlinecitation = article.parentNode
        paginationlist = medlinecitation.getElementsByTagName("pagination")
    
    str = ""
    
    if paginationlist.length > 0:
        pagination = paginationlist.item(0)
        str = pagination.getElementsByTagName("medlinepgn").item(0).firstChild.nodeValue
    
    return str


# retrieve date information for an article
def get_pubmed_article_date(journalissue):
    date = ""
    pubdatelist = journalissue.getElementsByTagName("pubdate")
    
    if pubdatelist.length > 0:
        pubdate = pubdatelist.item(0)
        medlinedatelist = pubdate.getElementsByTagName("medlinedate")
        
        if medlinedatelist.length > 0:
            date = medlinedatelist.item(0).firstChild.nodeValue
        else:
            year = pubdate.getElementsByTagName("year").item(0).firstChild.nodeValue
            month = ""
            # month may not be present in some cases
            monthlist = pubdate.getElementsByTagName("month")
            
            if monthlist.length > 0:
                month = monthlist.item(0).firstChild.nodeValue
                
            date = year + " " + month           
    else:
        pubdatelist = journalissue.getElementsByTagName("pubDate")
        
        if pubdatelist.length > 0:
            pubdate = pubdatelist.item(0)
            year = pubdate.getElementsByTagName("year").item(0).firstChild.nodeValue
            month = pubdate.getElementsByTagName("month").item(0).firstChild.nodeValue
            date = year + " " + month
    
    return date


#return the markup for a book article
def get_book_article_info(docroot):
    bookdocument = docroot.getElementsByTagName("bookdocument").item(0)
    book = bookdocument.getElementsByTagName("book").item(0)
    abstract = bookdocument.getElementsByTagName("abstract").item(0)
    sections = bookdocument.getElementsByTagName("sections").item(0)
    
    title = book.getElementsByTagName("booktitle").item(0).firstChild.nodeValue
    authors = get_book_article_authors(book)
    abstract = get_book_article_abstract(bookdocument)
    metadata = get_book_article_metadata(book)
    sections = get_book_article_sections(bookdocument)
    
    htmlstr = """
              <html>
              <head>
                <meta http-equiv="Content-type" content="text/html;charset=UTF-8"/>
                <title>%s</title>
                <style type="text/css">
                  h2 {
                    font-size: 24px;
                    margin-bottom: 5px;
                  }
                  
                  h3 {
                    font-size: 18px;
                    margin-bottom: 5px;
                  }
                  
                  p.first {
                    margin-top: 5px;
                  }
                </style>
              </head>
              <body>
                <h2>%s</h2>
                <div class='authors'>%s</div>
                <div class='metadata'>%s</div>
              """ % (title, title, authors, metadata)

        
    if abstract != "":
        htmlstr += "<h3>Excerpt</h3>"
        htmlstr += "<div class='excerpts'>%s</div>" % abstract
        
    if sections != "":
        htmlstr += "<h3>Sections</h3>"
        htmlstr += "<div class='sections'>%s</div>" % sections
              
    htmlstr += """
               </body>
               </html>
               """
               
    return htmlstr


# returns the author list for a book article
def get_book_article_authors(book):
    return get_pubmed_article_authors(book)
    

# returns the metadata (publisher etc) for a book article
def get_book_article_metadata(book):
    str = ""
    
    publisher = book.getElementsByTagName("publisher").item(0)
    name = publisher.getElementsByTagName("publishername").item(0).firstChild.nodeValue
    location = publisher.getElementsByTagName("publisherlocation").item(0).firstChild.nodeValue
    
    str = "%s: %s" % (location, name)
    str += "<br/>"
    
    collectiontitle = book.getElementsByTagName("collectiontitle").item(0).firstChild.nodeValue
    str += collectiontitle
    
    return str


# returns the abstract for a book article
def get_book_article_abstract(bookdocument):
    return get_pubmed_article_abstract(bookdocument)


# returns the list of sections for a book article
def get_book_article_sections(bookdocument):
    str = ""
    
    sections = bookdocument.getElementsByTagName("sections")
    sectionlist = sections.item(0).getElementsByTagName("section")
    
    for section in sectionlist:
        labellist = section.getElementsByTagName("locationlabel")
        label = ""
        
        if labellist.length > 0:
            label = labellist.item(0).firstChild.nodeValue
                    
        title = section.getElementsByTagName("sectiontitle").item(0).firstChild.nodeValue
        
        if label != "":
            str += "%s. %s" % (label, title)
        else:
            str += "%s" % title

        str += "<br/>"
           
    return str

            
# program execution starts here
if __name__ == "__main__":
    xmldoc = minidom.parse("ClinicalInquiries.xml")
    root = xmldoc.documentElement
    
    recordlist = root.getElementsByTagName("record")
    create_files(recordlist)
    
    
    
    
    
