z-img-desktop-updater
=====================

I use this to ping z-img.com with a search query and then parse their page for the image and set it as my backgroud. Could just as easily use Google, since that's what their sites using, but this was more fun. And linked off of /r/ScarlettJohansson.

##Example:

    main("Scarlett Johansson", 'zimg') #or 'bing' for Bing Images

looks up a random "Scarlett Johansson hot" image, and sets it as your background

    main()

does something similar, but instead pulls a name from `searches.txt` and uses
that as the query instead.

ISSUES:

    * If a request.get call fails, the whole thing crashes.
        * Handle exceptions
    * The search results are always the first page, so if you use this script
      too often, you'll always have the same pool of images
        * Figure out how to go to next page of search results,
          or get more images in one query

TODO:

    * Add ignore urls, so you don't get the same less desirable watermarks
    * Some sort of file organization or limit. Right now, there's not limit on
      the images it saves and keeps on your harddrive
    * Size limits. Can be any size deemed 'large' by the engine. It'd be nice
      to be able to specify dimensions
