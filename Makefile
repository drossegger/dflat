# You probably need to adjust the *_dir variables before running "make"
cxxflags_release="-DWITH_THREADS=0 -DPROGRESS_REPORT -DDISABLE_ANSWER_SET_CHECKS"
cxxflags_debug="-DWITH_THREADS=0 -DPROGRESS_REPORT -DWITH_NODE_TIMER -DPRINT_COMPUTED_ROWS -DPRINT_BAG_INPUT -DPRINT_MODELS -DPRINT_CHILD_TABLES_INPUT"
cxxflags_gprof=$(cxxflags_debug)

gringo_dir=/home/dino/workspace/bach-thesis/gringo-3.0.5-source
gringo_lib=$(gringo_dir)/build/release/lib/libgringo.a
gringo_lib_debug=$(gringo_dir)/build/debug/lib/libgringo.a
gringo_lib_gprof=$(gringo_dir)/build/gprof/lib/libgringo.a

clasp_dir=/home/dino/workspace/bach-thesis/clasp-2.1.1
clasp_lib=$(clasp_dir)/build/release/libclasp/lib/libclasp.a
clasp_lib_debug=$(clasp_dir)/build/debug/libclasp/lib/libclasp.a
clasp_lib_gprof=$(clasp_dir)/build/gprof/libclasp/lib/libclasp.a

sharp_dir=$(PWD)/sharp

all: release

release:
	mkdir -p build/release/parser
	cd build/release && \
	cmake ../../src \
		-DCMAKE_BUILD_TYPE=release \
		-DCMAKE_CXX_FLAGS:STRING=$(cxxflags_release) \
		-Dgringo_lib=$(gringo_lib) \
		-Dclasp_lib=$(clasp_lib) \
		-Dgringo_dir=$(gringo_dir) \
		-Dclasp_dir=$(clasp_dir) \
		-Dsharp_dir=$(sharp_dir) \
	&& $(MAKE)

debug:
	mkdir -p build/debug/parser
	cd build/debug && \
	cmake ../../src \
		-DCMAKE_BUILD_TYPE=debug \
		-DCMAKE_CXX_FLAGS:STRING=$(cxxflags_debug) \
		-Dgringo_lib=$(gringo_lib_debug) \
		-Dclasp_lib=$(clasp_lib_debug) \
		-Dgringo_dir=$(gringo_dir) \
		-Dclasp_dir=$(clasp_dir) \
		-Dsharp_dir=$(sharp_dir) \
	&& $(MAKE)

gprof:
	mkdir -p build/gprof/parser
	cd build/gprof && \
	cmake ../../src \
		-DCMAKE_BUILD_TYPE=gprof \
		-DCMAKE_CXX_FLAGS:STRING=$(cxxflags_gprof) \
		-Dgringo_lib=$(gringo_lib_gprof) \
		-Dclasp_lib=$(clasp_lib_gprof) \
		-Dgringo_dir=$(gringo_dir) \
		-Dclasp_dir=$(clasp_dir) \
		-Dsharp_dir=$(sharp_dir) \
	&& $(MAKE)

clean:
	rm -rf build
