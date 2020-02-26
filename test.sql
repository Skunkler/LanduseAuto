set linesize 500
set pagesize 400
COLUMN DATE_OUT_PLANNING FORMAT A9 HEADING DATE_OUT
COLUMN PROJECT_NO FORMAT A6 HEADING PROJID
COLUMN DEVELOPMENT_NAME FORMAT A50 HEADING NAME

spool D:\LandUseEdit\testrun2.txt




select b.PL_ID, a.PROJECT_NO, a.DATE_FINAL_REVIEW_COMP, a.PLAN_ENGR_ID, b.TOTAL_ONSITE_FIREFLOW, b.TOTAL_FIREFLOW, a.PZONE,
a.DEVELOPMENT_NAME from wdresplanlog.pl_global_search_wpp_v b, wdresplanlog.pl_water_packet a
where b.PL_ID = a.PL_ID(+)
and a.PROJECT_NO in (select w.project_no 
from wdresplanlog.pl_water_packet w, wdresplangis.landuse_evw g
where TO_NUMBER(w.project_no) = g.projid(+)
and g.projid is NULL
and w.DATE_OUT_PLANNING is NOT NULL
and w.DATE_IN_PLANNING >= '01-SEP-19')
ORDER BY a.project_no;

spool off
 


