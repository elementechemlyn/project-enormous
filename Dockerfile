ARG KONG_BASE_TAG
FROM kong${KONG_BASE_TAG}

USER root
ENV LUA_PATH /usr/local/share/lua/5.1/?.lua;/usr/local/kong-oidc/?.lua;;
# For lua-cjson
ENV LUA_CPATH /usr/local/lib/lua/5.1/?.so;;

# Install unzip for luarocks, gcc for lua-cjson
RUN apt-get update && apt-get install -y unzip gcc 
RUN luarocks install luacov
RUN luarocks install luaunit
RUN luarocks install lua-cjson

# Change openidc version when version in rockspec changes
RUN luarocks install lua-resty-openidc 1.6.0
COPY kong-oidc /usr/local/kong-oidc