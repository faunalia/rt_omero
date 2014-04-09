import os.path
from pyspatialite import dbapi2 as sqlite

def connect(path):
    path = unicode(path)
    if not os.path.exists( path.encode('utf8') ):
        raise IOError( u'"%s" not found' % path )

    return sqlite.connect( path )

sys_tables = [ "geom_cols_ref_sys", "geometry_columns", "geometry_columns_auth", 
        "views_geometry_columns", "virts_geometry_columns", "spatial_ref_sys", 
        "sqlite_sequence", #"tableprefix_metadata", "tableprefix_rasters", 
        "layer_params","layer_statistics", "layer_sub_classes", "layer_table_layout", 
        "pattern_bitmaps","symbol_bitmaps", "project_defs", "raster_pyramids", 
        "sqlite_stat1", "sqlite_stat2", "spatialite_history" ]


def get_tables(conn):
    tables = []
    idx_tables = []
    c = conn.cursor()
    # get the R*Tree tables
    sql = u"SELECT f_table_name, f_geometry_column FROM geometry_columns WHERE spatial_index_enabled = 1"
    c.execute(sql)        
    for idx_item in c.fetchall():
        idx_tables.append( 'idx_%s_%s' % idx_item )
        idx_tables.append( 'idx_%s_%s_node' % idx_item )
        idx_tables.append( 'idx_%s_%s_parent' % idx_item )
        idx_tables.append( 'idx_%s_%s_rowid' % idx_item )
    for tbl in c.fetchall():
        if tbl[0] in idx_tables:
            continue
        tables.append( tbl )

    sql = u"SELECT name FROM sqlite_master WHERE type = 'table'"
    c.execute(sql)
    for tbl in c.fetchall():
        if tbl[0] in sys_tables or tbl[0] in idx_tables:
            continue
        tables.append( tbl )
    return tables  # row = [tablename]

def get_table_fields(conn, table):
    """ return list of columns in table """
    c = conn.cursor()

    sql = u"PRAGMA table_info(%s)" % table
    c.execute(sql)  # row = [num, name, datatype, ...]
    return map(lambda x: x[1], c.fetchall())


def get_vector_tables(conn):
    tables = []
    idx_tables = []
    try:
        c = conn.cursor()

        # get the R*Tree tables
        sql = u"SELECT f_table_name, f_geometry_column FROM geometry_columns WHERE spatial_index_enabled = 1"
        c.execute(sql)
        for idx_item in c.fetchall():
            idx_tables.append( 'idx_%s_%s' % idx_item )
            idx_tables.append( 'idx_%s_%s_node' % idx_item )
            idx_tables.append( 'idx_%s_%s_parent' % idx_item )
            idx_tables.append( 'idx_%s_%s_rowid' % idx_item )

        # get geometry info from geometry_columns if exists
        sql = u"""SELECT m.name, g.f_table_name, g.f_geometry_column, g.type, g.coord_dimension, g.srid 
        FROM sqlite_master AS m JOIN geometry_columns AS g ON lower(m.name) = lower(g.f_table_name)
        WHERE m.type = 'table'"""
        c.execute(sql)
        for tbl in c.fetchall():
            if tbl[0] in sys_tables or tbl[0] in idx_tables:
                continue
            tables.append( tbl )
    except sqlite.Error:
        pass  # no geometry column...

    return tables  # row = [tablename, g_tablename, g_geomcol, g_type, g_dim, g_srid]


def merge(db1, db2):
    conn1 = connect(db1)
    conn2 = connect(db2)
    
    for tblinfo in get_vector_tables(conn1):
        merge_table(conn1, conn2, tblinfo, True)

    for tblinfo in get_tables(conn1):
        merge_table(conn1, conn2, tblinfo, False)

def merge_table(conn1, conn2, tblinfo, is_vector=False):
    tblname = tblinfo[0]
    if tblname.upper() in ('ZZ_DISCLAIMER', 'ZZ_WMS'):
        return

    fields = get_table_fields(conn1, tblname)
    fldnames = '"' + u'","'.join(fields) + '"'
    if is_vector:
        pos = fields.index(tblinfo[2])
        infldnames_str = '"' + u'","'.join(fields[:pos] + fields[pos+1:]) + '"' + u', ST_AsBinary("%(geom)s"), ST_SRID("%(geom)s")' % {'geom':tblinfo[2]}
        valplaces_str = u",".join("?" * pos) + u", ST_GeomFromWKB(?, ?)"
    else:
        infldnames_str = '"' + u'","'.join(fields) + '"'
        valplaces_str = u",".join("?"*len(fields))


    c1 = conn1.cursor()
    sql1 = u"SELECT %s FROM %s" % (infldnames_str, tblname)
    c1.execute(sql1)
    
	# allow to change tables
    c2 = conn2.cursor()
    c2.execute("UPDATE ZZ_DISCLAIMER SET ATTIVO=1");
	
	# dump and delete triggers
    triggersToMantain=["ZZ_COMUNI", "geometrie_unita_volumetriche_originali_di_partenza_geometria", "geometrie_rilevate_nuove_o_modificate_geometria"]
    triggers = []
    c2.execute(u"SELECT name, sql FROM sqlite_master WHERE lower(tbl_name) = lower('%s') AND type='trigger'" % tblname)
    for row in c2.fetchall():
        name, sql = row
        mantain = False
        for mantainedTrigger in triggersToMantain:
            if mantainedTrigger in name:
                mantain = True
        if mantain:
            continue
        triggers.append(row)
    for name, sql in triggers:
        c2.execute(u'DROP TRIGGER "%s"' % name)
	
    sql2 = u'INSERT OR IGNORE INTO "%s" (%s) VALUES (%s)' % (tblname, fldnames, valplaces_str)
    try:
        for row in c1.fetchall():
            c2.execute(sql2, row)
    except sqlite.Error:
        conn2.rollback()
        raise
    else:
        # restore triggers
        for name, sql in triggers:
            c2.execute(sql)
        # no more changes allowed
        c2.execute("UPDATE ZZ_DISCLAIMER SET ATTIVO=0");
        conn2.commit()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        sys.exit(1)

    merge(sys.argv[1], sys.argv[2])
    sys.exit(0)


