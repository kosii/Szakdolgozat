import pefile

class PE(pefile.PE):
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
        ordinal = get_sectionordinal_by_virtual_address(self, virtual_addr)
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
        section = pe.sections[ordinal]
        return phys_addr - section.PointerToRawData + self.OPTIONAL_HEADER.ImageBase + section.VirtualAddress

def get_sectionname_by_physical_address(pe, phys_addr):

    for section in pe.sections:
        if section.PointerToRawData <= phys_addr and phys_addr < section.PointerToRawData + section.SizeOfRawData:
            return section.Name
    return None

def get_sectionname_by_virtual_address(pe, virtual_address):

    for section in pe.sections:
        if pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress <= virtual_address and virtual_address < pe.OPTIONAL_HEADER.ImageBase + section.VirtualAddress + section.SizeOfRawData:
            return section.Name
    return None