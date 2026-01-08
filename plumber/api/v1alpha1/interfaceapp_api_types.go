/*
Copyright 2026.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

// InterfaceAppSpec defines the desired state of InterfaceApp
type InterfaceAppSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
	// +eda:ui:title="Nodes"
	// List of nodes on which to configure the banners.
	Nodes []string `json:"nodes,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Ports"
	// Idetify which ports to create ie, 1 - 3, 5 - 10
	PortSelector string `json:"portselector,omitempty"`
	// +eda:ui:orderpriority=300
	// +eda:ui:title="Enabled"
	// +kubebuilder:default=true
	Enabled bool `json:"enabled,omitempty"`
	// +kubebuilder:validation:Enum=lag;interface;loopback
	// +eda:ui:orderpriority=400
	// +eda:ui:title="Type"
	// +eda:ui:columnspan=2
	// +kubebuilder:default=interface
	// Type defines whether the interface is a Lag or Interface.
	Type string `json:"type,omitempty"`
	// +kubebuilder:validation:Enum=null;dot1q
	// +eda:ui:orderpriority=500
	// +eda:ui:title="Encapsulation Type"
	// +eda:ui:columnspan=2
	// +kubebuilder:default=null
	// Enable or disable VLAN tagging on this interface. [default="null"]
	EncapType string `json:"encapType,omitempty"`
	// +eda:ui:orderpriority=600
	// +eda:ui:title="LLDP"
	// +kubebuilder:default=true
	LLDP bool `json:"lldp,omitempty"`
	// +eda:ui:title="MTU"
	// MTU to apply on all interfaces
	MTU int `json:"mtu,omitempty"`
	// +kubebuilder:validation:Enum="1G";"10G";"25G";"40G";"50G";"100G";"400G"
	// +eda:ui:orderpriority=700
	// +eda:ui:title="Port Speed"
	// +eda:ui:columnspan=2
	// +kubebuilder:default="1G"
	// The speed of this interface, in human-readable format - e.g. 25G, 100G.
	Speed string `json:"speed,omitempty"`
}

// InterfaceAppStatus defines the observed state of InterfaceApp
type InterfaceAppStatus struct{}
