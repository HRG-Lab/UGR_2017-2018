LIBMAJ:=               3
LIBMIN:=               0
LIBREV:=               12

LIBFULLREV:=           $(LIBMAJ).$(LIBMIN).$(LIBREV)

LIBNAME:=              libxbee

MANDIR:=               man
HTMLDIR:=              html
BUILDDIR:=             .build
DESTDIR:=              lib
HDRDIR:=               include

CONSTRUCTIONDIRS:=     $(BUILDDIR) $(DESTDIR)

SYS_HEADERS:=          xbee.h xbeep.h

### the OS config can override this if any are incompatible
MODELIST:=             xbee1 xbee2 xbee3 xbee5 xbee6b xbeeZB net debug
