mkdir boost-subset
bcp --boost=.\boost_1_58_0 build test wave program_options property_tree signals2 locale inspect config circular_buffer spirit algorithm assign smart_ptr bimap logic phoenix uuid range utility icl chrono .\boost-subset

bcp --boost=.\boost_1_70_0 build test wave program_options property_tree signals2 locale inspect config circular_buffer spirit algorithm assign bimap logic phoenix uuid range utility icl .\boost_1_70_0-subset