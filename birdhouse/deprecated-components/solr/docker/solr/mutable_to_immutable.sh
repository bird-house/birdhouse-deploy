#!/bin/bash
 
# The path to the schema and config files must be specified in the
# SOLRCONFIGPATH env variable and the core name in SOLRCORE.
#export SOLRCONFIGPATH="/opt/solr/server/solr/core_name/conf"
#export SOLRCORE="core_name"
 
# This will slighly mess up the xml indentation & leave superfluous blank lines.
mv /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/managed-schema /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/schema.xml
if grep '<schemaFactory class="ManagedIndexSchemaFactory">' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
    then
        sed -i $'/<schemaFactory class="ManagedIndexSchemaFactory">/c\<schemaFactory class="ClassicIndexSchemaFactory"\/>' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
        sed -i $'/<bool name="mutable">true<\/bool>/c\ ' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
        sed -i $'/<str name="managedSchemaResourceName">managed-schema<\/str>/c\ ' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
        sed -i $'/<\/schemaFactory>/c\ ' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
    else
        sed -i $'/<config>/c\<config>\\n<schemaFactory class="ClassicIndexSchemaFactory"\/>' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
fi
if grep '<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
    then
        naddschema="""$(awk '/<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">/{ print NR; exit }' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml)"""
        nendprocessor="""$(awk "NR>$naddschema && /<\/processor>/ {print NR; exit}" /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml)"""
        sed -i "${nendprocessor}s/<\/processor>/<\/processor>-->/" /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
        sed -i '/<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">/c\<!--<processor class="solr.AddSchemaFieldsUpdateProcessorFactory">' /opt/conda/envs/birdhouse/var/lib/solr/birdhouse/conf/solrconfig.xml
fi
curl "http://localhost:8983/solr/admin/cores?action=RELOAD&core=birdhouse"
