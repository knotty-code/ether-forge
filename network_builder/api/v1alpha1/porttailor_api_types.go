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
	// +eda:ui:columnspan=3
	// +eda:ui:orderpriority=100
	// +eda:ui:title="Port List"
	// +eda:ui:autocomplete=`{"group":"network-builder.eda.local", "version":"v1alpha1", "resource":"portlibraries"}`
	// Select interface from Port Library.
	Ports []string `json:"ports,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=4
	// +eda:ui:orderpriority=200
	// +eda:ui:title="Port Description"
	// Add a meaningfull description for selected port(s).
	PortDescription string `json:"portDescription,omitempty"`
}

// PortTailorStatus defines the observed state of PortTailor
type PortTailorStatus struct {
	// +eda:ui:title="Nodes"
	// List of nodes this banner has been applied to
	Nodes []string `json:"nodes,omitempty"`
}
