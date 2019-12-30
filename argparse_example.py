import argparse
import sys

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-u', '--user',
                        help='user',
                        # required='True',
                        default='apiuser')
    parser.add_argument('-p', '--password',
                        help='password',
                        # required='True',
                        default='d0nthack')
    parser.add_argument('-a', '--account',
                        help='account',
                        # required='True',
                        default=None)
    parser.add_argument('-t', '--table',
                        help='table to insert result',
                        default='QUERIES')
    parser.add_argument('-w', '--warehouse',
                        help='warehouse',
                        default='EDW_I_OPS_WH')
    parser.add_argument('-d', '--database',
                        help='database',
                        default='DEMO_DB')
    parser.add_argument('-s', '--schema',
                        help='schema',
                        default='PUBLIC')

    results = parser.parse_args(args)
    return (results.user,
            results.password,
            results.account,
            results.table,
            results.warehouse,
            results.database,
            results.schema)

if __name__ == '__main__':
    user, password, account, table, warehouse, database, schema = check_arg(sys.argv[1:])
    print ('u =',user)
    print ('p =',password)
    print ('a =',account)
    print('t =', table)
    print('w =', warehouse)
    print('d =', database)
    print('s =', schema)