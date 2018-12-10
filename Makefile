NUM_SOURCES = 10
SRCS := $(shell rm -f test_*.cpp ; ./gen_source.py ${NUM_SOURCES})
OBJS := $(patsubst %.cpp,%.o,${SRCS})
CXXFLAGS += -m64 -Wall -fPIC
LDFLAGS += -shared -fPIC

BIN=test.so

.PHONY: .o .so ${BIN}

%.o: %.cpp
	time -p $(CXX) $(CXXFLAGS) -o $@ -c $<

all: distcc
	nm -A --defined --demangle $^| grep foo_

bin: ${BIN}

${BIN}: ${OBJS}
	$(CXX) -o $@ ${LDFLAGS} $^

show:
	@echo SRCS=${SRCS}
	@echo OBJS=${OBJS}

distcc:
	${MAKE} bin -j ${NUM_SOURCES} CXX='distcc ${PWD}/my_gcc' DISTCC_SKIP_LOCAL_RETRY=1 DISTCC_HOSTS='--randomize server_one/10 server_two/10 ' 

server:
	$$(which distccd) -j 40 --log-stderr --log-level=info --no-detach --allow 127.0.0.1/24 --enable-tcp-insecure

mon:
	watch -n.1 'cat /proc/loadavg; distccmon-text '

