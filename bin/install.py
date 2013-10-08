import os
import sys

def main(args):

    if '--dev' in args:
        use_devel_version = True
        ape_devel_arg = '--dev'
        args.remove('--dev')
        djpl_install = 'pip install -e git+https://github.com/henzk/django-productline.git#egg=django-productline'
        djpl_cm_install = 'pip install -e git+https://github.com/henzk/djpl-container-management.git#egg=djpl-container-management'
    else:
        use_devel_version = False
        ape_devel_arg = ''
        djpl_install = 'pip install django-productline'
        #FIXME with first PYPI release
        djpl_cm_install = 'pip install -e git+https://github.com/henzk/djpl-container-management.git#egg=djpl-container-management'

    slim=False
    if '--slim' in args:
        slim=True
        args.remove('--slim')

    #FIXME currently a dev version of cookiecutter is required
    djpl_cm_install += '; pip install -e git+https://github.com/audreyr/cookiecutter@5fb9b77869f43dfc1fb746701a32d7e68678092c#egg=cookiecutter-dev'

    if len(args) != 2:
        print 'Usage:'
        print
        print 'install.py [--dev] <APE_ROOT_DIR>'
        print
        print 'Creates an ape-root at APE_ROOT_DIR for your django product lines.'
        print 'The given directory must not exist already.'
        print
        print 'If --dev is given, this installs the latest development versions from git.'
        print 'Otherwise, the latest stable version of ape, django-productline and djpl-container-management are used from PYPI.'
        print
        print 'If --slim is given, the installation of django-productline(and transitive dependencies like django) are omitted.'
        print 'This option makes sense, if you use virtualenvs to separate the spl containers and therefore don`t need those packages in the ape root virtualenv.'
        sys.exit(1)

    webapps = args[1]
    webapps_dir = '%s/%s' % (os.getcwd(), webapps)

    cmds = (
        'wget -O - https://raw.github.com/henzk/ape/master/bin/bootstrape | python - %s %s; ' % (webapps, ape_devel_arg) + 
        'cd %s ; ' % webapps_dir +
        '. _ape/activape ; ' +
        djpl_cm_install + '; '
    )

    if not slim:
        cmds += djpl_install + '; '

    os.system('bash -c "%s deactivape"; ' % cmds)
    # add initenv on ape container level
    with open('%s/initenv' % webapps_dir, 'w+') as initenv:
        initenv.write('export APE_PREPEND_FEATURES="ape.container_mode djpl_container_management"')


if __name__ == '__main__':
    main(sys.argv)
