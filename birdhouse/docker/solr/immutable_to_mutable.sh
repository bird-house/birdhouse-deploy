#!/bin/bash
 
# The path to the schema and config files must be specified in the
# SOLRCONFIGPATH env variable and the core name in SOLRCORE.
#export SOLRCONFIGPATH="/opt/solr/server/solr/core_name/conf"
#export SOLRCORE="core_name"
 
# This will slighly mess up the xml indentation.
sed -i $'/<schemaFactory class="ClassicIndexSchemaFactory"\/>/c\<schemaFactory class="ManagedIndexSchemaFactory">\\n<bool name="mutable">true<\/bool>\\n<str name="managedSchemaResourceName">managed-schema<\/str>\\n<\/schemaFactory>' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
sed -i '/<\/processor>-->/c\<\/processor>' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
sed -i '/<!--<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">/c\<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
#curl "http://localhost:8983/solr/admin/cores?action=RELOAD&core=birdhouse"
