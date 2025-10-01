from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy
import os

class TinyMPCConan(ConanFile):
    name = "tinympc"
    version = "1.0.0"
    license = "Apache 2.0"
    author = "TinyMPC Team, Pedram Rabiee (prabiee@3laws.io)"
    url = "https://github.com/pedramrabiee/TinyMPC"
    description = "A high-speed Model Predictive Control (MPC) solver for microcontrollers"
    topics = ("mpc", "control", "optimization", "embedded", "robotics")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "shared": [True, False],
        "using_codegen": [True, False],
    }
    default_options = {
        "fPIC": True,
        "shared": False,
        "using_codegen": False,
    }

    package_type = "library"
    exports_sources = "CMakeLists.txt", "src/*", "LICENSE"

    def requirements(self):
        # Use external Eigen instead of bundled version
        self.requires("eigen/3.4.0")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_TESTING"] = False
        tc.variables["USING_CODEGEN"] = self.options.using_codegen
        tc.variables["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.get_safe("fPIC", True)
        # TinyMPC requires C++17
        tc.variables["CMAKE_CXX_STANDARD"] = 17
        tc.variables["CMAKE_CXX_STANDARD_REQUIRED"] = True
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        # Copy license
        copy(self, "LICENSE", src=self.source_folder,
             dst=os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.libs = ["tinympcstatic"]
        self.cpp_info.requires = ["eigen::eigen"]
        self.cpp_info.set_property("cmake_file_name", "tinympc")
        self.cpp_info.set_property("cmake_target_name", "tinympc::tinympcstatic")
