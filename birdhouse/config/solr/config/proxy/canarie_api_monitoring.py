SERVICES['node']['monitoring']['Solr'] = {
    'request': {
        'url': 'http://10.0.2.15:8983/solr/birdhouse/select?q=CMIP5&fq=model:MPI-ESM-MR&fq=experiment:rcp45&fq=variable:tasmax&fq=institute:MPI-M&fq=frequency:mon&wt=json'
    },
    'response': {
        'text': '.*catalog_url\":\".+/testdata/flyingpigeon/cmip5.*/catalog.xml.*'
    }
}
