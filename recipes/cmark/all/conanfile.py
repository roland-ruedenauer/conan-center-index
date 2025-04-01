from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, rmdir
import os


required_conan_version = ">=2.0.9"

class cmarkRecipe(ConanFile):
    name = "cmark"
    description = "CommonMark parsing and rendering library and program in C"
    license = "BSD2"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/commonmark/cmark"
    topics = ("commonmark", "markdown", "parser")
    package_type = "library"
    languages = ["C"]
    settings = "os", "arch", "compiler", "build_type"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True
    }

    implements = ["auto_shared_fpic"]

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.16 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination=self.source_folder,
            strip_root=True)
        apply_conandata_patches(self)

    def layout(self):
        cmake_layout(self, src_folder="src")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = bool(self.options.shared)
        tc.variables["BUILD_TESTING"] = False
        tc.variables["CMARK_LIB_FUZZER"] = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "cmark")
        self.cpp_info.set_property("cmake_target_name", "cmark::cmark")
        self.cpp_info.set_property("pkg_config_name", "cmark")
        self.cpp_info.bindirs = []
        self.cpp_info.libs = ["cmark"]
