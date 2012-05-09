import pefile

class PE(pefile.PE):
    
    def GetSectionnameOrdinal(self, section_name):
        section_name = section_name.ljust(8, '\0')
        for i, section in enumerate(self.sections):
            if section.Name == section_name:
                return i
        raise ValueError("Invalid section_name")

    def GetSectionnameSection(self, section_name):
        section_ordinal = self.GetSectionnameOrdinal(section_name)
        return self.sections[section_ordinal]
    
    def GetSectionnameContent(self, section_name):
        section = self.GetSectionnameSection(section_name)
        return section.get_data()
    
    def GetPhysicalAddressSectionOrdinal(self, phys_addr):
        for i, section in enumerate(self.sections):
            if section.PointerToRawData <= phys_addr < section.PointerToRawData + section.SizeOfRawData:
                return i
        raise ValueError("Invalid PhysicalAddress")
    
    def GetPhysicalAddressSectionName(self, phys_addr):
        ordinal = self.GetPhysicalAddressSectionOrdinal(phys_addr)
        return self.sections[ordinal].Name

    def GetVirtualAddressSectionOrdinal(self, virt_addr):
        for i, section in enumerate(self.sections):
            if self.OPTIONAL_HEADER.ImageBase + section.VirtualAddress <= virt_addr < self.OPTIONAL_HEADER.ImageBase + section.VirtualAddress + section.SizeOfRawData:
                return i
        raise ValueError("Invalid VirtualAddress")
    
    def GetVirtualAddressSectionName(self, virtual_addr):
        ordinal = self.GetVirtualAddressSectionOrdinal(virtual_addr)
        return self.sections[ordinal].Name
    
    def vtop(self, virt_addr):
        if not virt_addr:
            return 0
        ordinal = self.GetVirtualAddressSectionOrdinal(virt_addr)
        section = self.sections[ordinal]
        return virt_addr - self.OPTIONAL_HEADER.ImageBase - section.VirtualAddress + section.PointerToRawData 
    
    def ptov(self, phys_addr):
        if not phys_addr:
            return 0
        ordinal = self.GetPhysicalAddressSectionOrdinal(phys_addr)
        section = self.sections[ordinal]
        return phys_addr - section.PointerToRawData + self.OPTIONAL_HEADER.ImageBase + section.VirtualAddress
