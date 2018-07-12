#!/opt/mkkd/mkkd_venv/bin/python
# -*- coding: UTF-8 -*-
from jira import JIRA
from dcm_conf import config
import cx_Oracle
import pgdb


def jira_open_con():
    options = {'server': 'https://jiramkkd.atlassian.net'}
    meta_jira = config['jira']
    jira = JIRA(options=options, basic_auth=(meta_jira['login'], meta_jira['pass']))
    return jira


def ora_open_con():
    meta_db = config['ora_dcm']
    dsn = cx_Oracle.makedsn(host=meta_db['host'],
                            port=meta_db['port'],
                            sid=meta_db['sid'])
    conn_meta = cx_Oracle.connect(user=meta_db['user'],
                                  password=meta_db['pwd'],
                                  dsn=dsn)
    return conn_meta


def ora_get_data(con, sql):
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()

    return data


ora_con = ora_open_con()
jira = jira_open_con()


for i in ora_get_data(ora_con, '''SELECT * FROM (
                                        SELECT
                                        v_st.*,
                                        row_number()
                                          OVER (
                                          PARTITION BY SRC_CODE, PKG_ID, TGT_LAYER, PERIOD
                                          ORDER BY INSERT_DATE )rn
                                        FROM V_DQ_CS_STATE v_st
                                        WHERE CS_STATE = 'CHECKED' and notify_flag='N'
                                      )rn
                                      WHERE rn = 1
                                    '''):
    src_code = i[1]
    pkg_id = i[2]
    tgt_layer = i[3]
    period = i[4]
    issue_dict = {
        'project':'FP',
        'summary': 'Составить отчет по СИ ' + str(src_code) + ' слою ' + tgt_layer + '.',
        'description': 'Составить отчет по выверенным данным за период ' + period + 'по слою ' + tgt_layer + 'по СИ '
                       + src_code +' попакету '+str(pkg_id)+'.',
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    ora_get_data(ora_con,'''update (select notify_flag from dq_cs_state s
                                    join dq_cs c
                                        on s.cs_id=c.cs_id
                                    where c.src_code='{src}' and 
                                          c.pkg_id={pkg} and 
                                          c.tgt_layer='{layer}' and 
                                          c.period=to_date('{period}','yyyymmdd'))
                            set notify_flag='Y';
                ''').format(src = src_code,pkg = pkg_id, layer = tgt_layer,period = period )

# authed_jira = JIRA(auth=('telitsina_aa', 'Qaz!2345'))
# issue = jira.issue('DWM-5')
#issue = jira_open_con().search_issues('assignee=aatelitsina@gmail.com')
# new_issue = jira_open_con().create_issue(project='FP', summary='New issue from jira-python',
#                               description='Look into this one', issuetype={'name': 'Bug'})
#print(issue)
