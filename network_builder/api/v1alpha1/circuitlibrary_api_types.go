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

// CircuitLibrarySpec defines the desired state of CircuitLibrary
// +eda:ui:condition=`{"condition":"!(spec.nodes.length === 0 && spec.nodeSelector.length === 0)", "errorMsg":"Either nodes or nodeSelector must have at least one value set"}`
type CircuitLibrarySpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"core.eda.nokia.com", "version":"v1", "resource":"toponodes"}`
	// +eda:ui:title="Nodes"
	// List of nodes on which to configure the banners.
	Nodes []string `json:"nodes,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=150
	// +eda:ui:title="Port-B"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// Select interface from Port Library.
	PortA []string `json:"portA,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Port-A"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// Select interface from Port Library.
	PortB []string `json:"portB,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=250
	// +eda:ui:title="Supernet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetgenies"}`
	Supernet []string `json:"supernet,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:orderpriority=300
	// +eda:ui:columnspan=3
	// +eda:ui:title="Subnet"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"subnetlibraries"}`
	Subnet []string `json:"subnets,omitempty"`
}

// CircuitLibraryStatus defines the observed state of CircuitLibrary
type CircuitLibraryStatus struct {
	// +eda:ui:title="Nodes"
	// List of nodes this banner has been applied to
	Nodes []string `json:"nodes,omitempty"`
}
