def get_moudle_cur_abspath():
    approot = ''
    try:
        approot = op.dirname(op.abspath(__file__))
    except NameError:  # maybe We are the main py2exe script, not a module
        approot = op.dirname(op.abspath(sys.argv[0]))
    return approot