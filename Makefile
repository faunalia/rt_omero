UI_SOURCES=$(wildcard ui/*.ui)
UI_FILES=$(patsubst %.ui,%_ui.py,$(UI_SOURCES))

GEN_FILES = resources.py ${UI_FILES}

all: $(GEN_FILES)


$(UI_FILES): %_ui.py: %.ui
	pyuic4 -o $@ $<
	
resources.py: resources.qrc
	pyrcc4 -o resources.py resources.qrc


clean:
	rm -f $(GEN_FILES) *.pyc

package:
	cd .. && ln -sTf trunk rt_omero && rm -f rt_omero.zip && zip -r rt_omero.zip rt_omero -x \*.svn* -x \*.pyc -x \*~ -x \*entries\* -x \*.git\* && rm -f rt_omero
