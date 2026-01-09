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

// Listen up — this is Jack Burton in the Pork Chop Express,
// and InterfaceAppSpec is the rig that tells me what kinda freight you're haulin' across these nodes.
// You throw in your nodes, ports, speed, type — all the good stuff — and ol' Jack
// takes it from there, configurin' interfaces like thunder rollin' through Chinatown.
// It's all about gettin' the job done clean and mean, no fuss, no drift, just pure network power.
// You know what ol' Jack Burton says? It's all in the reflexes.
type InterfaceAppSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
	// +eda:ui:title="Nodes"
	// Tell ol' Jack which rigs (nodes) he needs to haul this config to. Pick one or twenty — I drive 'em all.
	Nodes []string `json:"nodes,omitempty"`

	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Ports"
	// Which ports we lightin' up today? Throw me somethin' like "1-3,5-10". I got this. It's all in the reflexes.
	PortSelector string `json:"portselector,omitempty"`

	// +eda:ui:orderpriority=300
	// +eda:ui:title="Enabled"
	// +kubebuilder:default=true
	// You want these interfaces up and runnin'? Hell yeah you do. Default's on — because Jack don't do half measures.
	Enabled bool `json:"enabled,omitempty"`

	// +kubebuilder:validation:Enum=lag;interface;loopback
	// +eda:ui:orderpriority=400
	// +eda:ui:title="Type"
	// +eda:ui:columnspan=2
	// +kubebuilder:default=interface
	// What kinda beast we buildin'? Regular interface, LAG bundle, or loopback? Default's plain interface — keep it simple, tall man.
	Type string `json:"type,omitempty"`

	// +kubebuilder:validation:Enum=null;dot1q
	// +eda:ui:orderpriority=500
	// +eda:ui:title="Encapsulation Type"
	// +eda:ui:columnspan=2
	// +kubebuilder:default=null
	// VLAN tagging or straight raw? Null means no tags — just pure freight. Dot1q if you wanna get fancy.
	EncapType string `json:"encapType,omitempty"`

	// +eda:ui:orderpriority=600
	// +eda:ui:title="LLDP"
	// +kubebuilder:default=true
	// Let the neighbors know who's boss. LLDP on by default — because Jack Burton don't hide in the shadows.
	LLDP bool `json:"lldp,omitempty"`

	// +eda:ui:title="MTU"
	// +kubebuilder:validation:Minimum=1450
	// +kubebuilder:validation:Maximum=9500
	// How big can the packets get before I gotta break 'em up? Throw me a number. Bigger's usually better.
	MTU int `json:"mtu,omitempty"`

	// +kubebuilder:validation:Enum="1G";"10G";"25G";"40G";"50G";"100G";"400G"
	// +eda:ui:orderpriority=700
	// +eda:ui:title="Port Speed"
	// +eda:ui:columnspan=2
	// +kubebuilder:default="1G"
	// How fast we haulin' this data? 1G's the default — reliable, like the Pork Chop Express. But you can go full thunder if you got the horsepower.
	Speed string `json:"speed,omitempty"`

	// +eda:ui:orderpriority=800
	// +eda:ui:title="DDM"
	// Enables reporting of DDM events.
	DDM bool `json:"ddm,omitempty"`
}

// InterfaceAppStatus defines the observed state of InterfaceApp
type InterfaceAppStatus struct{}
