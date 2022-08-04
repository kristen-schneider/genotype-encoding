#configfile: "config.yaml"

rule segment_vcf_COMPILE:
	input:
		main="cpp/src/main.cpp",
		read_config="cpp/src/read_config.cpp",
		include="cpp/include/"

	output:
		bin="cpp/bin/segment"

	shell:
		"g++ {input.main} {input.read_config} -I {input.include} -o {output.bin}"
