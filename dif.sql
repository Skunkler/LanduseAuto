select w.project_no, w.DATE_OUT_PLANNING, w.DEVELOPMENT_NAME
from wdresplanlog.pl_water_packet w, wdresplangis.landuse_evw g
where TO_NUMBER(w.project_no) = g.projid(+)
and g.projid is NULL
and w.DATE_OUT_PLANNING is NOT NULL
and w.DATE_IN_PLANNING >= (sysdate - 180)
ORDER BY w.project_no;





select b.PL_ID, a.PROJECT_NO from
wdresplanlog.pl_global_search_wpp_v b, wdresplanlog.pl_water_packet a
where b.PL_ID = a.PL_ID(+)
and a.PROJECT_NO in (select w.project_no 
from wdresplanlog.pl_water_packet w, wdresplangis.landuse_evw g
where TO_NUMBER(w.project_no) = g.projid(+)
and g.projid is NULL
and w.DATE_OUT_PLANNING is NOT NULL
and w.DATE_IN_PLANNING >= (sysdate - 180)
ORDER BY w.project_no;)



