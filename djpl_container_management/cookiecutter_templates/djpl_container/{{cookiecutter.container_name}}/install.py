from ape.installtools import cleanup, create_project_venv, fetch_pool, add_to_path

# cleanup the installation directory (_lib/)
cleanup()

# create a project-level virtualenv
venv = create_project_venv()

# install some requirements
venv.pip_install_requirements('requirements.txt')


# fetch some required feature pools
# fp = fetch_pool('<my git repository>')

# add everything to your pypath
add_to_path(
    venv.get_paths(),
    #fp.get_path(),
    # adds the features dir relative to your fp dir
    #fp.get_path('features')
)








