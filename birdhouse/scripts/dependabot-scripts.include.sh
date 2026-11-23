# Specifically exclude components that use images based on other component versions
# Add new components to the EXCLUDE_COMPONENTS list (one per line)
EXCLUDE_COMPONENTS='
components/twitcher
optional-components/generic_bird
optional-components/testthredds
optional-components/test-cowbird-jupyter-access
'
# A regular expression built from EXCLUDE_COMPONENTS that will match any of the components listed in EXCLUDE_COMPONENTS
EXCLUDE_COMPONENTS_RE="$(echo $EXCLUDE_COMPONENTS | sed 's/[[:space:]]/\\\|/g')"
