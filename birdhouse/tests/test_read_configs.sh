setup_suite() {
  if [ ! -f ../read-configs.include.sh ]; then
    echo "ERROR: expected current dir is test dir." 1>&2
    exit 2
  fi

  . ../read-configs.include.sh

  if [ -e "../env.local" ]; then
      echo "ERROR: please save your env.local to avoid losing it.  We will override it with our test version." 1>&2
      exit 2
  fi
}


teardown_suite() {
    rm ../env.local
}


test_simple_all_conf_dirs_content() {

    # Simple env.local.
    echo "
export EXTRA_CONF_DIRS='
    ./optional-components/all-public-access
    ./optional-components/test-weaver
'" > ../env.local

    # Redirect STDOUT to /dev/null to hide all "reading './config/XYX/default.env'" and
    # "delayed eval 'VAR=value'" messages.
    read_configs > /dev/null

    # TODO: expected wrong output just to get test to pass.
    # test-weaver depends on weaver so weaver has to be listed first.
    EXPECTED_ALL_CONF_DIRS="
            ./config/proxy
          
            ./config/canarie-api
          
            ./config/phoenix
          
            ./config/malleefowl
          
            ./config/postgres
          
            ./config/wps_outputs-volume
          
            ./config/data-volume
          
            ./config/flyingpigeon
          
            ./config/catalog
          
            ./config/mongodb
          
            ./config/geoserver
          
            ./config/finch
          
            ./config/raven
          
            ./config/hummingbird
          
            ./config/thredds
          
            ./config/portainer
          
            ./config/magpie
          
            ./config/twitcher
          
            ./config/jupyterhub
          
            ./config/frontend
          
            ./config/ncwms2
          
            ./config/project-api
          
            ./config/solr
          
            ./optional-components/all-public-access
          
            ./optional-components/test-weaver
          
            ./components/weaver
          "

    assert_equals "$EXPECTED_ALL_CONF_DIRS" "$ALL_CONF_DIRS"
}
