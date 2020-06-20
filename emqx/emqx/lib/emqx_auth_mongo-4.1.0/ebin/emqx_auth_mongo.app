{application,emqx_auth_mongo,
             [{description,"EMQ X Authentication/ACL with MongoDB"},
              {vsn,"4.1.0"},
              {modules,[emqx_acl_mongo,emqx_auth_mongo,emqx_auth_mongo_app,
                        emqx_auth_mongo_sup]},
              {registered,[emqx_auth_mongo_sup]},
              {applications,[kernel,stdlib,mongodb,ecpool,emqx_passwd]},
              {mod,{emqx_auth_mongo_app,[]}},
              {env,[]},
              {licenses,["Apache-2.0"]},
              {maintainers,["EMQ X Team <contact@emqx.io>"]},
              {links,[{"Homepage","https://emqx.io/"},
                      {"Github","https://github.com/emqx/emqx-auth-mongo"}]}]}.