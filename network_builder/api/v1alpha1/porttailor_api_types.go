/*
Copyright 2025.

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

// PortTailorSpec defines the desired state of PortTailor
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type PortTailorSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
	// +eda:ui:title="Nodes"
	// List of nodes on which to configure the banners.
	Nodes []string `json:"nodes,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Node Selector"
	// +eda:ui:format="labelselector"
	// Label selector to select nodes on which to configure the banners.
	NodeSelector []string `json:"nodeSelector,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=300
	// +eda:ui:title="Login Banner"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// This is the login banner displayed before a user has logged into the Node.
	LoginBanner []string `json:"loginBanner,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:title="Interface Pattern"
	// Regex or glob to match interface names (e.g., "ethernet-1/*")
	InterfacePattern string `json:"interfacePattern,omitempty"`
	// NEW FIELD: Let user select which PortLibrary instances to tailor
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=400
	// +eda:ui:title="Port Library Selector"
	// +eda:ui:format="labelselector"
	// Select derived PortLibrary resources to apply additional configuration to
	PortLibrarySelector []string `json:"portLibrarySelector,omitempty"`
}

// PortTailorStatus defines the observed state of PortTailor
type PortTailorStatus struct {
	// +eda:ui:title="Nodes"
	// List of nodes this banner has been applied to
	Nodes []string `json:"nodes,omitempty"`
}
