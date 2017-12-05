from ast import literal_eval
from pandas import DataFrame
import re
import requests
import subprocess
import sys

corpora = {'eng_us_2012': 17, 'eng_us_2009': 5, 'eng_gb_2012': 18,
           'eng_gb_2009': 6, 'eng_2012': 15, 'eng_2009': 0,
           'eng_fiction_2012': 16, 'eng_fiction_2009': 4, 'eng_1m_2009': 1}


def setup_params(argument_string):
    arguments_list = argument_string.split()

    phrases = ' '.join(
        [arg for arg in arguments_list if not arg.startswith('-')])

    cmd_options = [arg for arg in arguments_list if arg.startswith('-')]

    remote_params = {'content': phrases, 'corpus': 'eng_2012',
                     'year_start': 1900, 'year_end': 2008, 'smoothing': 3}
    local_params = {'printHelp': False, 'allData': False, 'toSave': True,
                    'toPrint': True, 'toPlot': False}

    # parsing the phrases parameters
    for option in cmd_options:
        if '-nosave' in option:
            local_params['toSave'] = False
        elif '-noprint' in option:
            local_params['toPrint'] = False
        elif '-plot' in option:
            local_params['toPlot'] = True
        elif '-corpus' in option:
            remote_params['corpus'] = option.split('=')[1].strip()
        elif '-startYear' in option:
            remote_params['year_start'] = int(option.split('=')[1])
        elif '-endYear' in option:
            remote_params['year_end'] = int(option.split('=')[1])
        elif '-smoothing' in option:
            remote_params['smoothing'] = int(option.split('=')[1])
        elif '-caseInsensitive' in option:
            remote_params['caseInsensitive'] = True
        elif '-alldata' in option:
            remote_params['allData'] = True
        else:
            print(('Did not recognize the following argument: %s' % option))

    return remote_params, local_params


def get_ngrams(req_params):
    req = requests.get('http://books.google.com/ngrams/graph',
                       params=req_params)

    # Return all non-overlapping matches of pattern in string, as a list of
    # strings. In this case only one group can be found res[0]
    res = re.findall('var data = (.*?);\\n', req.text)
    if res:
        data = {response['ngram']: response['timeseries']
                for response in literal_eval(res[0])}

        df = DataFrame(data)
        print(df.head())
        start_year = req_params['year_start']
        end_year = req_params['year_end']
        df.insert(0, 'year', list(range(start_year, end_year + 1)))
        print(df.head())
    else:
        df = DataFrame()
    return req.url, req_params['content'], df


def run_query(argument_string):
    req_params, local_params = setup_params(argument_string)

    url, urlquery, df = get_ngrams(req_params)
    if not local_params['allData']:
        if 'caseInsensitive' in local_params:
            for col in df.columns:
                if col.count('(All)') == 1:
                    df[col.replace(' (All)', '')] = df.pop(col)

                elif col.count('(All)') == 0 and col != 'year':
                    if col not in urlquery.split(','):
                        df.pop(col)

    if local_params['toPrint']:
        print((','.join(df.columns.tolist())))
        for row in df.iterrows():
            try:
                print(('%d,' % int(row[1].values[0]) +
                       ','.join(['%.12f' % s for s in row[1].values[1:]])))
            except:
                print((','.join([str(s) for s in row[1].values])))

    queries = ''.join(urlquery.replace(',', '_').split())

    if 'caseInsensitive' in local_params:
        word_case = 'caseInsens'
    else:
        word_case = 'caseSens'
    filename = '{0}-{1}-{2}-{3}-{4}-{5}.csv'.\
        format(queries, req_params['corpus'],
               req_params['year_start'], req_params['year_end'],
               req_params['smoothing'], word_case)

    if local_params['toSave']:
        for col in df.columns:
            if '&gt;' in col:
                df[col.replace('&gt;', '>')] = df.pop(col)
        df.to_csv(filename, index=False)
        print(('Data saved to %s' % filename))

    if local_params['toPlot']:
        try:
            subprocess.call(['python3', 'pandasPlot.py', filename])
        except:
            if not local_params['toSave']:
                print(('Currently, if you want to create a plot you ' +
                       'must also save the data. Rerun your phrases, ' +
                       'removing the -nosave option.'))
            else:
                print(('Plotting Failed: %s' % filename))


if __name__ == '__main__':
    argument_string = ' '.join(sys.argv[1:])
    try:
        run_query(argument_string)
    except:
        print('An error occurred.')
